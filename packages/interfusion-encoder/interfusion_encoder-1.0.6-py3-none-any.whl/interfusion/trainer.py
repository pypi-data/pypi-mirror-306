# interfusion/trainer.py

import os
import random
import time
import numpy as np
from collections import defaultdict

import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torch.cuda.amp import GradScaler
from transformers import AutoTokenizer, AutoModel

# Set environment variables and multiprocessing start method at the very beginning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import torch.multiprocessing as mp
try:
    mp.set_start_method('spawn', force=True)
except RuntimeError:
    # The start method has already been set
    pass

from .models import CrossEncoderModel, compute_bi_encoder_embeddings
from .data_utils import CrossEncoderDataset, set_seed
from .config import get_default_config

# Dummy tqdm for environments where tqdm is not desired
class DummyTqdm:
    def __init__(self, iterable=None, **kwargs):
        self.iterable = iterable if iterable is not None else []
        self.iterator = iter(self.iterable)
        self.desc = kwargs.get('desc', '')
        self.start_time = None
        self.end_time = None

    def __iter__(self):
        self.start_time = time.time()
        return self

    def __next__(self):
        try:
            return next(self.iterator)
        except StopIteration:
            self.end_time = time.time()
            total_time = self.end_time - self.start_time
            if self.desc:
                print(f"{self.desc} completed in {total_time:.2f} seconds")
            else:
                print(f"Iteration completed in {total_time:.2f} seconds")
            raise

    def __getattr__(self, attr):
        # Return a dummy function for any other attributes
        return lambda *args, **kwargs: None

    def update(self, n=1):
        pass

    def set_description(self, desc=None, refresh=True):
        pass

    def close(self):
        pass


def get_tqdm(config):
    if not config.get('use_tqdm', True):
        return DummyTqdm
    else:
        tqdm_type = config.get('tqdm_type', 'standard')
        try:
            if tqdm_type == 'notebook':
                from tqdm.notebook import tqdm
            else:
                from tqdm import tqdm
        except ImportError:
            print("tqdm is not installed. Progress bars will be disabled.")
            return DummyTqdm
        return tqdm


class HardNegativeDataset(Dataset):
    def __init__(self, hard_negatives, job_id_to_text, use_sparse=False, candidate_feature_size=0, job_feature_size=0):
        """
        Initialize the HardNegativeDataset.

        Args:
            hard_negatives (dict): Dictionary containing hard negatives per candidate.
            job_id_to_text (dict): Mapping from job_id to job_text.
            use_sparse (bool): Whether to use sparse features.
            candidate_feature_size (int): Size of candidate features.
            job_feature_size (int): Size of job features.
        """
        self.hard_negatives = hard_negatives
        self.job_id_to_text = job_id_to_text
        self.use_sparse = use_sparse
        self.candidate_feature_size = candidate_feature_size
        self.job_feature_size = job_feature_size
        self.pairs = []
        self.prepare_pairs()

    def prepare_pairs(self):
        """
        Prepare pairs of (candidate_id, candidate_text, job_text, candidate_features, job_features).
        """
        for cid, neg in self.hard_negatives.items():
            job_ids = neg['job_ids']
            job_texts = neg['job_texts']
            if self.use_sparse:
                job_features = neg.get('job_features', [None] * len(job_ids))
                for jid, j_text, j_feat in zip(job_ids, job_texts, job_features):
                    self.pairs.append((cid, j_text, j_feat))
            else:
                for jid, j_text in zip(job_ids, job_texts):
                    self.pairs.append((cid, j_text, None))

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        """
        Retrieve the sample at index `idx`.

        Returns:
            tuple: (candidate_id, job_text, job_features)
        """
        return self.pairs[idx]

    def collate_fn(self, batch):
        """
        Custom collate function to handle batches of (cid, j_text, j_feat).

        Returns:
            dict: Contains lists of candidate_ids, job_texts, and job_features.
        """
        candidate_ids, job_texts, job_features = zip(*batch)
        return {
            'candidate_ids': list(candidate_ids),
            'job_texts': list(job_texts),
            'job_features': list(job_features)
        }


class CrossEncoderEvalDataset(Dataset):
    def __init__(self, candidate_texts, job_texts):
        self.candidate_texts = candidate_texts
        self.job_texts = job_texts

    def __len__(self):
        return len(self.candidate_texts)

    def __getitem__(self, idx):
        return (self.candidate_texts[idx], self.job_texts[idx])


def train_model(candidates, jobs, positive_matches, candidates_eval=None, jobs_eval=None, positive_matches_eval=None, user_config=None):
    """
    Train the InterFusion Encoder model.

    Parameters:
    - candidates: list of dictionaries representing candidates.
    - jobs: list of dictionaries representing jobs.
    - positive_matches: list of dictionaries representing positive matches.
    - candidates_eval: (optional) list of dictionaries representing evaluation candidates.
    - jobs_eval: (optional) list of dictionaries representing evaluation jobs.
    - positive_matches_eval: (optional) list of dictionaries representing evaluation positive matches.
    - user_config: (optional) dictionary to override default configurations.
    """

    # Merge user configuration with default configuration
    config = get_default_config()
    if user_config:
        config.update(user_config)

    # Initialize logging frameworks if enabled
    if config.get('use_wandb', False):
        import wandb
        wandb.init(project=config.get('wandb_project', 'InterFusion'), name=config.get('wandb_run_name', 'run'), config=config)
    elif config.get('use_mlflow', False):
        import mlflow
        mlflow.start_run()
        mlflow.log_params(config)

    set_seed(config['random_seed'])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Create directory to save models
    os.makedirs(config['save_dir'], exist_ok=True)

    # Build mappings
    candidate_id_to_text = {candidate['candidate_id']: candidate['candidate_text'] for candidate in candidates}
    candidate_id_to_features = {candidate['candidate_id']: candidate.get('candidate_features', None) for candidate in candidates}
    job_id_to_text = {job['job_id']: job['job_text'] for job in jobs}
    job_id_to_features = {job['job_id']: job.get('job_features', None) for job in jobs}

    if candidates_eval is None:
        # If evaluation data is not provided, use the training data
        candidates_eval = candidates
        jobs_eval = jobs
        positive_matches_eval = positive_matches

    # Build data_samples
    data_samples = []
    for match in positive_matches:
        candidate_id = match['candidate_id']
        job_id = match['job_id']
        data_samples.append({
            'candidate_id': candidate_id,
            'candidate_text': candidate_id_to_text[candidate_id],
            'positive_job_id': job_id,
            'positive_job_text': job_id_to_text[job_id],
            'candidate_features': candidate_id_to_features.get(candidate_id, None),
            'positive_job_features': job_id_to_features.get(job_id, None)
        })

    # Initialize tokenizer
    tokenizer = AutoTokenizer.from_pretrained(config['cross_encoder_model_name'])

    # Initialize bi-encoder
    bi_encoder = AutoModel.from_pretrained(config['bi_encoder_model_name']).to(device)

    # Implement triangular learning rate scheduler with non-zero starting LR
    lr_start = config['initial_learning_rate']
    lr_max = config['learning_rate']
    num_epochs = config['num_epochs']
    start_mult = lr_start / lr_max  # Multiplier at epoch 0

    def lr_lambda(epoch):
        if epoch <= num_epochs / 2:
            return start_mult + (1.0 - start_mult) * (epoch / (num_epochs / 2))
        else:
            return start_mult + (1.0 - start_mult) * ((num_epochs - epoch) / (num_epochs / 2))

    # If using sparse features, set feature sizes
    candidate_feature_size = 0
    job_feature_size = 0
    if config['use_sparse']:
        # Verify that all candidates and jobs have 'candidate_features' and 'job_features'
        if all('candidate_features' in candidate for candidate in candidates) and all('job_features' in job for job in jobs):
            candidate_feature_lengths = [len(candidate['candidate_features']) for candidate in candidates]
            job_feature_lengths = [len(job['job_features']) for job in jobs]
            candidate_feature_size = max(candidate_feature_lengths)
            job_feature_size = max(job_feature_lengths)
            print(f"Candidate feature size detected and set to: {candidate_feature_size}")
            print(f"Job feature size detected and set to: {job_feature_size}")
        else:
            raise ValueError("All candidates and jobs must have 'candidate_features' and 'job_features' when 'use_sparse' is True.")

    # Load saved model if continue_training is True
    if config.get('continue_training', False):
        saved_model_path = config.get('saved_model_path', None)
        if saved_model_path and os.path.exists(saved_model_path):
            print(f"Loading saved model from {saved_model_path} for continued training...")
            checkpoint = torch.load(saved_model_path, map_location=device)

            # Initialize model
            model = CrossEncoderModel(config, candidate_feature_size, job_feature_size).to(device)

            # Load model state dict
            if 'model_state_dict' in checkpoint:
                model.load_state_dict(checkpoint['model_state_dict'])
                print("Model state dict loaded.")
            else:
                model.load_state_dict(checkpoint)
                print("Loaded model directly from checkpoint (no 'model_state_dict' key).")

            # Initialize optimizer, scheduler, and scaler
            optimizer = optim.AdamW(model.parameters(), lr=config['learning_rate'])
            scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)
            scaler = GradScaler()

            # Load optimizer and scheduler states if available
            if 'optimizer_state_dict' in checkpoint:
                optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
                print("Optimizer state dict loaded.")
            else:
                print("Optimizer state dict not found in checkpoint.")

            if 'scheduler_state_dict' in checkpoint:
                scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
                print("Scheduler state dict loaded.")
            else:
                print("Scheduler state dict not found in checkpoint.")

            if 'scaler_state_dict' in checkpoint:
                scaler.load_state_dict(checkpoint['scaler_state_dict'])
                print("Scaler state dict loaded.")
            else:
                print("Scaler state dict not found in checkpoint.")

            start_epoch = checkpoint.get('epoch', 0) + 1
            print(f"Resuming training from epoch {start_epoch}")
        else:
            print("Saved model path does not exist. Starting training from scratch.")
            start_epoch = 0
            # Initialize model, optimizer, scheduler, and scaler
            model = CrossEncoderModel(config, candidate_feature_size, job_feature_size).to(device)
            optimizer = optim.AdamW(model.parameters(), lr=config['learning_rate'])
            scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)
            scaler = GradScaler()
    else:
        print("Starting training from scratch.")
        start_epoch = 0
        # Initialize model, optimizer, scheduler, and scaler
        model = CrossEncoderModel(config, candidate_feature_size, job_feature_size).to(device)
        optimizer = optim.AdamW(model.parameters(), lr=config['learning_rate'])
        scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)
        scaler = GradScaler()

    # Precompute negatives using bi-encoder
    print("Precomputing negatives using bi-encoder...")
    negatives = precompute_bi_encoder_negatives(bi_encoder, tokenizer, candidates, jobs, positive_matches, config)

    # Generate initial hard negatives
    print("Generating initial hard negatives...")
    hard_negatives = generate_hard_negatives(model, data_samples, tokenizer, negatives, config, candidate_feature_size, job_feature_size)

    # Precompute N random negatives per candidate
    print("Precomputing random negatives...")
    random_negatives = precompute_random_negatives(candidates, jobs, positive_matches, config)

    # Initialize dataset with initial hard negatives and random negatives
    train_dataset = CrossEncoderDataset(
        data_samples, tokenizer, config, negatives=negatives,
        hard_negatives=hard_negatives, random_negatives=random_negatives
    )
    train_dataset.update_hard_negatives(hard_negatives)
    train_dataset.update_random_negatives(random_negatives)

    best_metric = 0.0  # Initialize best metric (e.g., Precision@5)
    tqdm_cls = get_tqdm(config)
    for epoch in range(start_epoch, num_epochs):
        print(f"\n=== Epoch {epoch + 1}/{num_epochs} ===")

        # Resample random negatives every epoch
        print("Resampling random negatives...")
        random_negatives = precompute_random_negatives(candidates, jobs, positive_matches, config)
        train_dataset.update_random_negatives(random_negatives)

        # Regenerate hard negatives every specified frequency
        if (epoch + 1) % config['hard_negative_sampling_frequency'] == 0:
            print(f"Generating hard negatives for epoch {epoch + 1}...")
            hard_negatives = generate_hard_negatives(model, data_samples, tokenizer, negatives, config, candidate_feature_size, job_feature_size)
            train_dataset.update_hard_negatives(hard_negatives)

        # Train for one epoch
        train(model, train_dataset, optimizer, device, config, epoch, scaler, scheduler)

        # Evaluate the model at specified epochs
        if (epoch + 1) % config.get('eval_epoch', 1) == 0:
            avg_precisions = evaluate(model, tokenizer, candidates_eval, jobs_eval, positive_matches_eval, config, bi_encoder, epoch)
            # Check if Precision@5 improved
            if 5 in avg_precisions:
                current_metric = avg_precisions[5]  # Precision at 5
                if current_metric > best_metric:
                    best_metric = current_metric
                    # Save the model
                    model_save_path = os.path.join(config['save_dir'], f"interfusion_best_p5_{best_metric:.4f}.pt")
                    torch.save({
                        'epoch': epoch,
                        'model_state_dict': model.state_dict(),
                        'optimizer_state_dict': optimizer.state_dict(),
                        'scheduler_state_dict': scheduler.state_dict(),
                        'scaler_state_dict': scaler.state_dict(),
                    }, model_save_path)
                    print(f"New best Precision@5: {best_metric:.4f}. Model saved to {model_save_path}")
                    # Log model checkpoint to W&B or MLflow if enabled
                    if config.get('use_wandb', False):
                        wandb.save(model_save_path)
                    elif config.get('use_mlflow', False):
                        mlflow.log_artifact(model_save_path)
            else:
                print("Precision@5 not available in evaluation results.")

    # Optionally, save the final model
    final_model_save_path = os.path.join(config['save_dir'], "interfusion_final.pt")
    torch.save({
        'epoch': num_epochs - 1,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'scheduler_state_dict': scheduler.state_dict(),
        'scaler_state_dict': scaler.state_dict(),
    }, final_model_save_path)
    print(f"Final model saved to {final_model_save_path}")

    # Finish logging frameworks
    if config.get('use_wandb', False):
        wandb.finish()
    elif config.get('use_mlflow', False):
        mlflow.end_run()


def precompute_bi_encoder_negatives(bi_encoder, tokenizer, candidates, jobs, positive_matches, config):
    """
    Precompute negatives using the bi-encoder by computing similarities and selecting top negatives.
    Optimized with vectorized operations and batching.
    """
    tqdm_cls = get_tqdm(config)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    bi_encoder.to(device)
    bi_encoder.eval()

    candidate_texts = [candidate['candidate_text'] for candidate in candidates]
    candidate_ids = [candidate['candidate_id'] for candidate in candidates]
    job_texts = [job['job_text'] for job in jobs]
    job_ids = [job['job_id'] for job in jobs]

    # Compute embeddings in batches
    print("Computing candidate embeddings...")
    candidate_embeddings = compute_bi_encoder_embeddings(bi_encoder, tokenizer, candidate_texts, config)
    print("Computing job embeddings...")
    job_embeddings = compute_bi_encoder_embeddings(bi_encoder, tokenizer, job_texts, config)

    # Normalize embeddings
    candidate_embeddings = nn.functional.normalize(candidate_embeddings, p=2, dim=1)
    job_embeddings = nn.functional.normalize(job_embeddings, p=2, dim=1)

    # Move embeddings to CPU for similarity computation
    candidate_embeddings = candidate_embeddings.cpu()
    job_embeddings = job_embeddings.cpu()

    # Compute similarity matrix
    print("Computing similarity matrix...")
    similarity_matrix = torch.matmul(candidate_embeddings, job_embeddings.t()).numpy()  # Shape: [num_candidates, num_jobs]

    # Build positive matches set
    positive_pairs = defaultdict(set)
    for match in positive_matches:
        positive_pairs[match['candidate_id']].add(match['job_id'])

    M = config['M']
    use_sparse = config['use_sparse']

    # Initialize negatives dictionary
    negatives = defaultdict(dict)

    # Vectorized masking of positive pairs
    print("Masking positive pairs in similarity matrix...")
    # Create a mask matrix where positive pairs are True
    mask = np.zeros_like(similarity_matrix, dtype=bool)
    for cid, jids in positive_pairs.items():
        if cid in candidate_ids:
            cid_idx = candidate_ids.index(cid)
            jid_indices = [job_ids.index(jid) for jid in jids if jid in job_ids]
            mask[cid_idx, jid_indices] = True
    # Set similarities of positive pairs to -inf
    similarity_matrix[mask] = -np.inf

    # Get top M negatives per candidate starting from start_rank
    print("Selecting top M negatives per candidate...")
    start_rank = config.get('start_rank', 1000)
    end_rank = start_rank + M
    num_candidates, num_jobs = similarity_matrix.shape

    # Handle cases where start_rank exceeds number of jobs
    valid_start_rank = min(start_rank, num_jobs)
    valid_end_rank = min(end_rank, num_jobs)

    # Use argpartition for efficient top-k selection
    top_m_indices = np.argpartition(-similarity_matrix, valid_end_rank - 1, axis=1)[:, start_rank:valid_end_rank]  # Shape: [num_candidates, M]

    # Retrieve job_ids and job_texts based on indices
    top_m_job_ids = np.take(job_ids, top_m_indices, axis=0)  # Shape: [num_candidates, M]
    top_m_job_texts = np.take(job_texts, top_m_indices, axis=0)  # Shape: [num_candidates, M]

    # Populate the negatives dictionary
    for idx, cid in tqdm_cls(enumerate(candidate_ids), total=len(candidate_ids), desc="Populating negatives"):
        neg_ids = top_m_job_ids[idx].tolist()
        neg_texts = top_m_job_texts[idx].tolist()
        negatives[cid]['job_ids'] = neg_ids
        negatives[cid]['job_texts'] = neg_texts

        if use_sparse:
            neg_features = [jobs[job_ids.index(jid)].get('job_features', None) for jid in neg_ids]
            negatives[cid]['job_features'] = neg_features

    return negatives


def generate_hard_negatives(model, data_samples, tokenizer, negatives, config, candidate_feature_size, job_feature_size):
    """
    Generate hard negatives by scoring precomputed negatives and selecting top N for each candidate.
    Utilizes DataLoader for efficient batching.
    """
    tqdm_cls = get_tqdm(config)

    model.eval()
    device = next(model.parameters()).device
    N = config['N']
    batch_size = config['negative_batch_size']
    use_sparse = config['use_sparse']

    # Create a dataset for hard negatives
    hard_neg_dataset = HardNegativeDataset(hard_negatives=negatives, job_id_to_text={jid: jtext for jid, jtext in zip([job['job_id'] for job in jobs], [job['job_text'] for job in jobs])}, use_sparse=use_sparse, candidate_feature_size=candidate_feature_size, job_feature_size=job_feature_size)
    hard_neg_dataloader = DataLoader(
        hard_neg_dataset,
        batch_size=batch_size,
        shuffle=False,
        collate_fn=hard_neg_dataset.collate_fn,
        num_workers=config['num_workers'],
        pin_memory=True
    )

    candidate_negatives = defaultdict(list)
    candidate_scores = defaultdict(list)

    with torch.no_grad():
        for batch in tqdm_cls(hard_neg_dataloader, desc="Generating hard negatives"):
            candidate_ids = batch['candidate_ids']
            job_texts = batch['job_texts']
            job_features = batch['job_features']

            inputs = tokenizer(job_texts, padding=True, truncation=True, max_length=config['max_length'], return_tensors='pt').to(device)

            if use_sparse:
                # Prepare and concatenate features
                candidate_features = []
                job_features_tensor = []
                for cf, jf in zip(batch['c_feats'], job_features):
                    if cf is not None:
                        cf_tensor = torch.tensor(cf, dtype=torch.float)
                    else:
                        cf_tensor = torch.zeros(candidate_feature_size)
                    candidate_features.append(cf_tensor)
                    if jf is not None:
                        jf_tensor = torch.tensor(jf, dtype=torch.float)
                    else:
                        jf_tensor = torch.zeros(job_feature_size)
                    job_features_tensor.append(jf_tensor)
                candidate_features = torch.stack(candidate_features).to(device)
                job_features_tensor = torch.stack(job_features_tensor).to(device)
                # Concatenate candidate and job features if required
                features_tensor = torch.cat((candidate_features, job_features_tensor), dim=1)  # Shape: [batch_size, candidate_feature_size + job_feature_size]
                logits = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], features=features_tensor)
            else:
                logits = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])

            batch_scores = logits.cpu().numpy()

            for cid, j_text, score in zip(candidate_ids, job_texts, batch_scores):
                candidate_negatives[cid].append({
                    'job_text': j_text,
                    'score': score
                })

    # Select top N hard negatives per candidate based on scores
    hard_negatives = {}
    for cid, neg_list in candidate_negatives.items():
        # Sort the negatives by score in descending order
        sorted_negatives = sorted(neg_list, key=lambda x: x['score'], reverse=True)
        top_n_negatives = sorted_negatives[:N]
        job_texts = [neg['job_text'] for neg in top_n_negatives]
        job_ids = [next((jid for jid, jtext in zip([job['job_id'] for job in jobs], [job['job_text'] for job in jobs]) if jtext == jt), None) for jt in job_texts]
        if use_sparse:
            job_features = [neg.get('job_features', None) for neg in top_n_negatives]
            hard_negatives[cid] = {
                'job_ids': job_ids,
                'job_texts': job_texts,
                'job_features': job_features
            }
        else:
            hard_negatives[cid] = {
                'job_ids': job_ids,
                'job_texts': job_texts
            }

    return hard_negatives  # Return the hard negatives separately


def precompute_random_negatives(candidates, jobs, positive_matches, config):
    """
    Precompute N random negatives per candidate.
    """
    job_ids = [job['job_id'] for job in jobs]
    job_id_to_text = {job['job_id']: job['job_text'] for job in jobs}
    job_id_to_features = {job['job_id']: job.get('job_features', None) for job in jobs}
    positive_job_ids_per_candidate = defaultdict(set)
    for match in positive_matches:
        cid = match['candidate_id']
        jid = match['job_id']
        positive_job_ids_per_candidate[cid].add(jid)
    N = config['N']
    use_sparse = config['use_sparse']
    random_negatives = {}
    for candidate in candidates:
        cid = candidate['candidate_id']
        positive_jids = positive_job_ids_per_candidate.get(cid, set())
        negative_jids = list(set(job_ids) - positive_jids)
        if len(negative_jids) >= N:
            sampled_neg_jids = random.sample(negative_jids, N)
        else:
            sampled_neg_jids = random.choices(negative_jids, k=N)
        neg_job_texts = [job_id_to_text[jid] for jid in sampled_neg_jids]
        if use_sparse:
            neg_features_list = [job_id_to_features[jid] for jid in sampled_neg_jids]
        else:
            neg_features_list = [None] * len(sampled_neg_jids)
        random_negatives[cid] = {
            'job_ids': sampled_neg_jids,
            'job_texts': neg_job_texts
        }
        if use_sparse:
            random_negatives[cid]['job_features'] = neg_features_list  # Store features here under candidate_id
    return random_negatives


def train(model, train_dataset, optimizer, device, config, epoch, scaler, scheduler):
    """
    Training function with mixed precision and listwise ranking loss.
    Utilizes DataLoader for efficient batching.
    """
    tqdm_cls = get_tqdm(config)

    model.train()
    train_dataloader = DataLoader(
        train_dataset,
        batch_size=config['train_batch_size'],  # Number of data samples per batch
        shuffle=True,
        collate_fn=train_dataset.collate_fn,
        num_workers=config['num_workers'],
        pin_memory=True
    )
    total_loss = 0
    criterion = nn.CrossEntropyLoss()
    for batch in tqdm_cls(train_dataloader, desc=f"Training Epoch {epoch+1}"):
        candidate_ids = batch['candidate_ids']
        job_texts = batch['job_texts']
        job_features = batch['job_features']

        # Generate labels: 1 for positive samples, 0 for negatives
        # Assuming that the first sample in each group is the positive sample
        # Modify this logic based on your actual data structure
        labels = torch.zeros(len(candidate_ids), dtype=torch.long).to(device)

        inputs = tokenizer(job_texts, padding=True, truncation=True, max_length=config['max_length'], return_tensors='pt').to(device)

        if config['use_sparse']:
            # Prepare and concatenate features
            candidate_features = []
            job_features_tensor = []
            for cf, jf in zip([train_dataset.hard_negatives[cid]['job_features'][0] if config['use_sparse'] else None for cid in candidate_ids],
                             [jf for jf in job_features]):
                if cf is not None:
                    cf_tensor = torch.tensor(cf, dtype=torch.float)
                else:
                    cf_tensor = torch.zeros(config['candidate_feature_size'])
                candidate_features.append(cf_tensor)
                if jf is not None:
                    jf_tensor = torch.tensor(jf, dtype=torch.float)
                else:
                    jf_tensor = torch.zeros(config['job_feature_size'])
                job_features_tensor.append(jf_tensor)
            candidate_features = torch.stack(candidate_features).to(device)
            job_features_tensor = torch.stack(job_features_tensor).to(device)
            # Concatenate candidate and job features if required
            features_tensor = torch.cat((candidate_features, job_features_tensor), dim=1)  # Shape: [batch_size, candidate_feature_size + job_feature_size]
            logits = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], features=features_tensor)
        else:
            logits = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])

        # Assume that the first job in each candidate's list is the positive job
        # Adjust this if your data structure is different
        # Create a mapping from candidate_id to indices in the batch
        candidate_to_indices = defaultdict(list)
        for idx, cid in enumerate(candidate_ids):
            candidate_to_indices[cid].append(idx)

        loss = 0.0
        for cid, indices in candidate_to_indices.items():
            candidate_logits = logits[indices]  # Shape: [num_samples]
            # Assume that the first index is the positive sample
            target = torch.tensor([0], dtype=torch.long).to(device)  # Positive sample at index 0
            loss += criterion(candidate_logits.unsqueeze(0), target)

        if len(candidate_to_indices) > 0:
            loss = loss / len(candidate_to_indices)
        else:
            loss = torch.tensor(0.0, requires_grad=True).to(device)

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        optimizer.zero_grad()
        total_loss += loss.item()

    avg_loss = total_loss / len(train_dataloader)
    print(f"Average training loss: {avg_loss:.4f}")
    # Update learning rate
    scheduler.step()
    current_lr = scheduler.get_last_lr()[0]
    print(f"Current learning rate: {current_lr:.6f}")
    # Log training loss and learning rate to W&B or MLflow if enabled
    if config.get('use_wandb', False):
        wandb.log({"Training Loss": avg_loss, "Learning Rate": current_lr, "Epoch": epoch + 1})
    elif config.get('use_mlflow', False):
        mlflow.log_metric("Training Loss", avg_loss, step=epoch + 1)
        mlflow.log_metric("Learning Rate", current_lr, step=epoch + 1)


def evaluate(model, tokenizer, candidates_eval, jobs_eval, positive_matches_eval, config, bi_encoder, epoch):
    """
    Evaluate the model using both bi-encoder and cross-encoder metrics.
    Utilizes vectorized operations and DataLoaders for efficiency.
    """
    tqdm_cls = get_tqdm(config)

    model.eval()
    device = next(model.parameters()).device
    Ns = config['eval_Ns']
    K = config.get('eval_K', 50)  # Number of top jobs to retrieve using bi-encoder

    # Build candidate and job texts and IDs
    candidate_texts = [candidate['candidate_text'] for candidate in candidates_eval]
    candidate_ids = [candidate['candidate_id'] for candidate in candidates_eval]
    job_texts = [job['job_text'] for job in jobs_eval]
    job_ids = [job['job_id'] for job in jobs_eval]

    # Create mappings from IDs to features
    candidate_id_to_features = {candidate['candidate_id']: candidate.get('candidate_features', None) for candidate in candidates_eval}
    job_id_to_features = {job['job_id']: job.get('job_features', None) for job in jobs_eval}

    # Create a mapping from job_text to job_id
    job_text_to_id = {job['job_text']: job['job_id'] for job in jobs_eval}

    # Create a mapping from candidate_id to ground truth job_ids
    candidate_to_jobs = defaultdict(set)
    for match in positive_matches_eval:
        cid = match['candidate_id']
        jid = match['job_id']
        candidate_to_jobs[cid].add(jid)

    # Compute embeddings using bi-encoder
    print("Computing candidate embeddings for evaluation...")
    candidate_embeddings = compute_bi_encoder_embeddings(bi_encoder, tokenizer, candidate_texts, config)
    print("Computing job embeddings for evaluation...")
    job_embeddings = compute_bi_encoder_embeddings(bi_encoder, tokenizer, job_texts, config)

    # Normalize embeddings
    candidate_embeddings = nn.functional.normalize(candidate_embeddings, p=2, dim=1)
    job_embeddings = nn.functional.normalize(job_embeddings, p=2, dim=1)

    # Compute similarity scores between all candidates and jobs
    similarities = torch.matmul(candidate_embeddings, job_embeddings.t()).cpu().numpy()  # Shape: [num_candidates, num_jobs]

    ### Evaluation using bi-encoder similarities ###
    print("\nEvaluating using bi-encoder similarities...")
    precisions_at_N_bi = {N: [] for N in Ns}
    for idx, candidate_id in tqdm_cls(enumerate(candidate_ids), total=len(candidate_ids), desc="Bi-Encoder Evaluation"):
        sim_scores = similarities[idx]  # Similarities for this candidate to all jobs
        # Get indices sorted by similarity in descending order
        sorted_indices = np.argsort(-sim_scores)
        sorted_job_ids = [job_ids[i] for i in sorted_indices]
        ground_truth_job_ids = candidate_to_jobs.get(candidate_id, set())
        for N in Ns:
            top_N_job_ids = sorted_job_ids[:N]
            hits = ground_truth_job_ids.intersection(top_N_job_ids)
            precision = len(hits) / N
            precisions_at_N_bi[N].append(precision)

    # Compute average precision at each N for bi-encoder
    avg_precisions_bi = {}
    print("\nAverage Precision at N using bi-encoder:")
    for N in Ns:
        avg_precision = np.mean(precisions_at_N_bi[N]) if precisions_at_N_bi[N] else 0.0
        avg_precisions_bi[N] = avg_precision
        print(f"Precision@{N}: {avg_precision:.4f}")

    ### Proceed with cross-encoder evaluation ###
    # For each candidate, get top K jobs and prepare cross-encoder inputs
    all_candidate_texts = []
    all_job_texts = []
    all_candidate_ids = []
    all_candidate_features = []
    all_job_features = []

    print("\nPreparing cross-encoder evaluation data...")
    for idx, candidate_id in tqdm_cls(enumerate(candidate_ids), total=len(candidate_ids), desc="Preparing Cross-Encoder Data"):
        sim_scores = similarities[idx]
        top_k_indices = np.argpartition(-sim_scores, K-1)[:K]
        top_k_job_texts = [job_texts[i] for i in top_k_indices]
        top_k_job_ids = [job_ids[i] for i in top_k_indices]
        candidate_text = candidate_texts[idx]
        candidate_feature = candidate_id_to_features.get(candidate_id, None)
        num_jobs = len(top_k_job_texts)
        all_candidate_texts.extend([candidate_text] * num_jobs)
        all_candidate_features.extend([candidate_feature] * num_jobs)
        all_job_texts.extend(top_k_job_texts)
        job_features = [job_id_to_features.get(job_id, None) for job_id in top_k_job_ids]
        all_job_features.extend(job_features)
        all_candidate_ids.extend([candidate_id] * num_jobs)

    # Create a dataset for cross-encoder evaluation
    eval_dataset = CrossEncoderEvalDataset(all_candidate_texts, all_job_texts)
    eval_dataloader = DataLoader(eval_dataset, batch_size=config['eval_batch_size'], shuffle=False, num_workers=config['num_workers'], pin_memory=True)

    print("\nEvaluating with cross-encoder...")
    scores = []
    model.eval()
    with torch.no_grad():
        for batch in tqdm_cls(eval_dataloader, desc="Cross-Encoder Evaluation"):
            c_texts, j_texts = batch
            inputs = tokenizer(c_texts, j_texts, max_length=config['max_length'], truncation=True, padding=True, return_tensors='pt').to(device)
            if config['use_sparse']:
                # Prepare and concatenate features
                candidate_features = torch.stack([
                    torch.tensor(cf, dtype=torch.float) if cf is not None else torch.zeros(config['candidate_feature_size'])
                    for cf in all_candidate_features
                ]).to(device)
                job_features = torch.stack([
                    torch.tensor(jf, dtype=torch.float) if jf is not None else torch.zeros(config['job_feature_size'])
                    for jf in all_job_features
                ]).to(device)
                # Concatenate candidate and job features if required
                features_tensor = torch.cat((candidate_features, job_features), dim=1)  # Shape: [batch_size, candidate_feature_size + job_feature_size]
                logits = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], features=features_tensor)
            else:
                logits = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])
            batch_scores = logits.cpu().numpy()
            scores.extend(batch_scores.tolist())

    # Collect scores per candidate
    candidate_job_scores = defaultdict(list)
    candidate_job_ids = defaultdict(list)
    for cid, jid, score in zip(all_candidate_ids, all_job_texts, scores):
        candidate_job_scores[cid].append(score)
        candidate_job_ids[cid].append(job_text_to_id[jid])

    # Compute precision at N using cross-encoder
    print("\nComputing Precision@N using cross-encoder scores...")
    precisions_at_N_cross = {N: [] for N in Ns}
    for candidate_id in tqdm_cls(candidate_ids, desc="Calculating Precision@N"):
        job_scores = candidate_job_scores[candidate_id]
        job_ids_list = candidate_job_ids[candidate_id]
        sorted_indices = np.argsort(-np.array(job_scores))
        sorted_job_ids = [job_ids_list[i] for i in sorted_indices]
        ground_truth_job_ids = candidate_to_jobs.get(candidate_id, set())
        for N in Ns:
            top_N_job_ids = sorted_job_ids[:N]
            hits = ground_truth_job_ids.intersection(top_N_job_ids)
            precision = len(hits) / N
            precisions_at_N_cross[N].append(precision)

    # Compute average precision at each N for cross-encoder
    avg_precisions = {}
    print("\nAverage Precision at N using cross-encoder:")
    for N in Ns:
        avg_precision = np.mean(precisions_at_N_cross[N]) if precisions_at_N_cross[N] else 0.0
        avg_precisions[N] = avg_precision
        print(f"Precision@{N}: {avg_precision:.4f}")

    # Log evaluation metrics to W&B or MLflow if enabled
    metrics = {f"Precision@{N}": avg_precisions[N] for N in Ns}
    metrics.update({f"BiEncoder Precision@{N}": avg_precisions_bi[N] for N in Ns})
    metrics["Epoch"] = epoch + 1

    if config.get('use_wandb', False):
        wandb.log(metrics)
    elif config.get('use_mlflow', False):
        for key, value in metrics.items():
            mlflow.log_metric(key, value, step=epoch + 1)

    return avg_precisions


def precompute_bi_encoder_negatives(bi_encoder, tokenizer, candidates, jobs, positive_matches, config):
    """
    Precompute negatives using the bi-encoder by computing similarities and selecting top negatives.
    Optimized with vectorized operations and batching.
    """
    tqdm_cls = get_tqdm(config)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    bi_encoder.to(device)
    bi_encoder.eval()

    candidate_texts = [candidate['candidate_text'] for candidate in candidates]
    candidate_ids = [candidate['candidate_id'] for candidate in candidates]
    job_texts = [job['job_text'] for job in jobs]
    job_ids = [job['job_id'] for job in jobs]

    # Compute embeddings in batches
    print("Computing candidate embeddings...")
    candidate_embeddings = compute_bi_encoder_embeddings(bi_encoder, tokenizer, candidate_texts, config)
    print("Computing job embeddings...")
    job_embeddings = compute_bi_encoder_embeddings(bi_encoder, tokenizer, job_texts, config)

    # Normalize embeddings
    candidate_embeddings = nn.functional.normalize(candidate_embeddings, p=2, dim=1)
    job_embeddings = nn.functional.normalize(job_embeddings, p=2, dim=1)

    # Move embeddings to CPU for similarity computation
    candidate_embeddings = candidate_embeddings.cpu()
    job_embeddings = job_embeddings.cpu()

    # Compute similarity matrix
    print("Computing similarity matrix...")
    similarity_matrix = torch.matmul(candidate_embeddings, job_embeddings.t()).numpy()  # Shape: [num_candidates, num_jobs]

    # Build positive matches set
    positive_pairs = defaultdict(set)
    for match in positive_matches:
        positive_pairs[match['candidate_id']].add(match['job_id'])

    M = config['M']
    use_sparse = config['use_sparse']

    # Initialize negatives dictionary
    negatives = defaultdict(dict)

    # Vectorized masking of positive pairs
    print("Masking positive pairs in similarity matrix...")
    # Create a mask matrix where positive pairs are True
    mask = np.zeros_like(similarity_matrix, dtype=bool)
    for cid, jids in positive_pairs.items():
        if cid in candidate_ids:
            cid_idx = candidate_ids.index(cid)
            jid_indices = [job_ids.index(jid) for jid in jids if jid in job_ids]
            mask[cid_idx, jid_indices] = True
    # Set similarities of positive pairs to -inf
    similarity_matrix[mask] = -np.inf

    # Get top M negatives per candidate starting from start_rank
    print("Selecting top M negatives per candidate...")
    start_rank = config.get('start_rank', 1000)
    end_rank = start_rank + M
    num_candidates, num_jobs = similarity_matrix.shape

    # Handle cases where start_rank exceeds number of jobs
    valid_start_rank = min(start_rank, num_jobs)
    valid_end_rank = min(end_rank, num_jobs)

    # Use argpartition for efficient top-k selection
    top_m_indices = np.argpartition(-similarity_matrix, valid_end_rank - 1, axis=1)[:, start_rank:valid_end_rank]  # Shape: [num_candidates, M]

    # Retrieve job_ids and job_texts based on indices
    top_m_job_ids = np.take(job_ids, top_m_indices, axis=0)  # Shape: [num_candidates, M]
    top_m_job_texts = np.take(job_texts, top_m_indices, axis=0)  # Shape: [num_candidates, M]

    # Populate the negatives dictionary
    for idx, cid in tqdm_cls(enumerate(candidate_ids), total=len(candidate_ids), desc="Populating negatives"):
        neg_ids = top_m_job_ids[idx].tolist()
        neg_texts = top_m_job_texts[idx].tolist()
        negatives[cid]['job_ids'] = neg_ids
        negatives[cid]['job_texts'] = neg_texts

        if use_sparse:
            neg_features = [jobs[job_ids.index(jid)].get('job_features', None) for jid in neg_ids]
            negatives[cid]['job_features'] = neg_features

    return negatives


def generate_hard_negatives(model, data_samples, tokenizer, negatives, config, candidate_feature_size, job_feature_size):
    """
    Generate hard negatives by scoring precomputed negatives and selecting top N for each candidate.
    Utilizes DataLoader for efficient batching.
    """
    tqdm_cls = get_tqdm(config)

    model.eval()
    device = next(model.parameters()).device
    N = config['N']
    batch_size = config['negative_batch_size']
    use_sparse = config['use_sparse']

    # Create a dataset for hard negatives
    # Prepare a mapping from job_id to job_text for easy lookup
    job_id_to_text = {job['job_id']: job['job_text'] for job in jobs}
    hard_neg_dataset = HardNegativeDataset(
        hard_negatives=negatives,
        job_id_to_text=job_id_to_text,
        use_sparse=use_sparse,
        candidate_feature_size=candidate_feature_size,
        job_feature_size=job_feature_size
    )
    hard_neg_dataloader = DataLoader(
        hard_neg_dataset,
        batch_size=batch_size,
        shuffle=False,
        collate_fn=hard_neg_dataset.collate_fn,
        num_workers=config['num_workers'],
        pin_memory=True
    )

    candidate_negatives = defaultdict(list)
    candidate_scores = defaultdict(list)

    with torch.no_grad():
        for batch in tqdm_cls(hard_neg_dataloader, desc="Generating hard negatives"):
            candidate_ids = batch['candidate_ids']
            job_texts = batch['job_texts']
            job_features = batch['job_features']

            # Tokenize the job texts
            inputs = tokenizer(job_texts, padding=True, truncation=True, max_length=config['max_length'], return_tensors='pt').to(device)

            if use_sparse:
                # Prepare and concatenate features
                candidate_features = []
                job_features_tensor = []
                for cf, jf in zip([negatives[cid]['candidate_features'] for cid in candidate_ids], job_features):
                    if cf is not None:
                        cf_tensor = torch.tensor(cf, dtype=torch.float)
                    else:
                        cf_tensor = torch.zeros(candidate_feature_size)
                    candidate_features.append(cf_tensor)
                    if jf is not None:
                        jf_tensor = torch.tensor(jf, dtype=torch.float)
                    else:
                        jf_tensor = torch.zeros(job_feature_size)
                    job_features_tensor.append(jf_tensor)
                candidate_features = torch.stack(candidate_features).to(device)
                job_features_tensor = torch.stack(job_features_tensor).to(device)
                # Concatenate candidate and job features if required
                features_tensor = torch.cat((candidate_features, job_features_tensor), dim=1)  # Shape: [batch_size, candidate_feature_size + job_feature_size]
                logits = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], features=features_tensor)
            else:
                logits = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])

            batch_scores = logits.cpu().numpy()

            for cid, j_text, score in zip(candidate_ids, job_texts, batch_scores):
                candidate_negatives[cid].append({
                    'job_text': j_text,
                    'score': score
                })

    # Select top N hard negatives per candidate based on scores
    hard_negatives = {}
    for cid, neg_list in candidate_negatives.items():
        # Sort the negatives by score in descending order
        sorted_negatives = sorted(neg_list, key=lambda x: x['score'], reverse=True)
        top_n_negatives = sorted_negatives[:N]
        job_texts = [neg['job_text'] for neg in top_n_negatives]
        # Map job_text back to job_id
        job_ids = [next((jid for jid, jtext in zip([job['job_id'] for job in jobs], [job['job_text'] for job in jobs]) if jtext == jt), None) for jt in job_texts]
        if use_sparse:
            job_features = [neg.get('job_features', None) for neg in top_n_negatives]
            hard_negatives[cid] = {
                'job_ids': job_ids,
                'job_texts': job_texts,
                'job_features': job_features
            }
        else:
            hard_negatives[cid] = {
                'job_ids': job_ids,
                'job_texts': job_texts
            }

    return hard_negatives  # Return the hard negatives separately


def precompute_random_negatives(candidates, jobs, positive_matches, config):
    """
    Precompute N random negatives per candidate.
    """
    job_ids = [job['job_id'] for job in jobs]
    job_id_to_text = {job['job_id']: job['job_text'] for job in jobs}
    job_id_to_features = {job['job_id']: job.get('job_features', None) for job in jobs}
    positive_job_ids_per_candidate = defaultdict(set)
    for match in positive_matches:
        cid = match['candidate_id']
        jid = match['job_id']
        positive_job_ids_per_candidate[cid].add(jid)
    N = config['N']
    use_sparse = config['use_sparse']
    random_negatives = {}
    for candidate in candidates:
        cid = candidate['candidate_id']
        positive_jids = positive_job_ids_per_candidate.get(cid, set())
        negative_jids = list(set(job_ids) - positive_jids)
        if len(negative_jids) >= N:
            sampled_neg_jids = random.sample(negative_jids, N)
        else:
            sampled_neg_jids = random.choices(negative_jids, k=N)
        neg_job_texts = [job_id_to_text[jid] for jid in sampled_neg_jids]
        if use_sparse:
            neg_features_list = [job_id_to_features[jid] for jid in sampled_neg_jids]
        else:
            neg_features_list = [None] * len(sampled_neg_jids)
        random_negatives[cid] = {
            'job_ids': sampled_neg_jids,
            'job_texts': neg_job_texts
        }
        if use_sparse:
            random_negatives[cid]['job_features'] = neg_features_list  # Store features here under candidate_id
    return random_negatives


def train(model, train_dataset, optimizer, device, config, epoch, scaler, scheduler):
    """
    Training function with mixed precision and listwise ranking loss.
    Utilizes DataLoader for efficient batching.
    """
    tqdm_cls = get_tqdm(config)

    model.train()
    train_dataloader = DataLoader(
        train_dataset,
        batch_size=config['train_batch_size'],  # Number of data samples per batch
        shuffle=True,
        collate_fn=train_dataset.collate_fn,
        num_workers=config['num_workers'],
        pin_memory=True
    )
    total_loss = 0
    criterion = nn.CrossEntropyLoss()
    for batch in tqdm_cls(train_dataloader, desc=f"Training Epoch {epoch+1}"):
        candidate_ids = batch['candidate_ids']
        job_texts = batch['job_texts']
        job_features = batch['job_features']

        # Tokenize the job texts
        inputs = tokenizer(job_texts, padding=True, truncation=True, max_length=config['max_length'], return_tensors='pt').to(device)

        if config['use_sparse']:
            # Prepare and concatenate features
            candidate_features = []
            job_features_tensor = []
            for cid, jf in zip(candidate_ids, job_features):
                cf = train_dataset.hard_negatives[cid].get('candidate_features', None)
                if cf is not None:
                    cf_tensor = torch.tensor(cf, dtype=torch.float)
                else:
                    cf_tensor = torch.zeros(config['candidate_feature_size'])
                candidate_features.append(cf_tensor)
                if jf is not None:
                    jf_tensor = torch.tensor(jf, dtype=torch.float)
                else:
                    jf_tensor = torch.zeros(config['job_feature_size'])
                job_features_tensor.append(jf_tensor)
            candidate_features = torch.stack(candidate_features).to(device)
            job_features_tensor = torch.stack(job_features_tensor).to(device)
            # Concatenate candidate and job features if required
            features_tensor = torch.cat((candidate_features, job_features_tensor), dim=1)  # Shape: [batch_size, candidate_feature_size + job_feature_size]
            logits = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], features=features_tensor)
        else:
            logits = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])

        # Generate labels: 1 for positive samples, 0 for negatives
        # Here, it's assumed that each candidate has one positive and N negatives
        # Modify this logic based on your actual data structure
        labels = torch.zeros(logits.size(0), dtype=torch.long).to(device)
        # Assuming the first sample for each candidate is the positive
        for i, cid in enumerate(candidate_ids):
            labels[i] = 1  # Set all to positive for simplicity; adjust as needed

        # Compute loss
        loss = criterion(logits, labels)

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        optimizer.zero_grad()
        total_loss += loss.item()

    avg_loss = total_loss / len(train_dataloader)
    print(f"Average training loss: {avg_loss:.4f}")
    # Update learning rate
    scheduler.step()
    current_lr = scheduler.get_last_lr()[0]
    print(f"Current learning rate: {current_lr:.6f}")
    # Log training loss and learning rate to W&B or MLflow if enabled
    if config.get('use_wandb', False):
        wandb.log({"Training Loss": avg_loss, "Learning Rate": current_lr, "Epoch": epoch + 1})
    elif config.get('use_mlflow', False):
        mlflow.log_metric("Training Loss", avg_loss, step=epoch + 1)
        mlflow.log_metric("Learning Rate", current_lr, step=epoch + 1)


def evaluate(model, tokenizer, candidates_eval, jobs_eval, positive_matches_eval, config, bi_encoder, epoch):
    """
    Evaluate the model using both bi-encoder and cross-encoder metrics.
    Utilizes vectorized operations and DataLoaders for efficiency.
    """
    tqdm_cls = get_tqdm(config)

    model.eval()
    device = next(model.parameters()).device
    Ns = config['eval_Ns']
    K = config.get('eval_K', 50)  # Number of top jobs to retrieve using bi-encoder

    # Build candidate and job texts and IDs
    candidate_texts = [candidate['candidate_text'] for candidate in candidates_eval]
    candidate_ids = [candidate['candidate_id'] for candidate in candidates_eval]
    job_texts = [job['job_text'] for job in jobs_eval]
    job_ids = [job['job_id'] for job in jobs_eval]

    # Create mappings from IDs to features
    candidate_id_to_features = {candidate['candidate_id']: candidate.get('candidate_features', None) for candidate in candidates_eval}
    job_id_to_features = {job['job_id']: job.get('job_features', None) for job in jobs_eval}

    # Create a mapping from job_text to job_id
    job_text_to_id = {job['job_text']: job['job_id'] for job in jobs_eval}

    # Create a mapping from candidate_id to ground truth job_ids
    candidate_to_jobs = defaultdict(set)
    for match in positive_matches_eval:
        cid = match['candidate_id']
        jid = match['job_id']
        candidate_to_jobs[cid].add(jid)

    # Compute embeddings using bi-encoder
    print("Computing candidate embeddings for evaluation...")
    candidate_embeddings = compute_bi_encoder_embeddings(bi_encoder, tokenizer, candidate_texts, config)
    print("Computing job embeddings for evaluation...")
    job_embeddings = compute_bi_encoder_embeddings(bi_encoder, tokenizer, job_texts, config)

    # Normalize embeddings
    candidate_embeddings = nn.functional.normalize(candidate_embeddings, p=2, dim=1)
    job_embeddings = nn.functional.normalize(job_embeddings, p=2, dim=1)

    # Compute similarity scores between all candidates and jobs
    similarities = torch.matmul(candidate_embeddings, job_embeddings.t()).cpu().numpy()  # Shape: [num_candidates, num_jobs]

    ### Evaluation using bi-encoder similarities ###
    print("\nEvaluating using bi-encoder similarities...")
    precisions_at_N_bi = {N: [] for N in Ns}
    for idx, candidate_id in tqdm_cls(enumerate(candidate_ids), total=len(candidate_ids), desc="Bi-Encoder Evaluation"):
        sim_scores = similarities[idx]  # Similarities for this candidate to all jobs
        # Get indices sorted by similarity in descending order
        sorted_indices = np.argsort(-sim_scores)
        sorted_job_ids = [job_ids[i] for i in sorted_indices]
        ground_truth_job_ids = candidate_to_jobs.get(candidate_id, set())
        for N in Ns:
            top_N_job_ids = sorted_job_ids[:N]
            hits = ground_truth_job_ids.intersection(top_N_job_ids)
            precision = len(hits) / N
            precisions_at_N_bi[N].append(precision)

    # Compute average precision at each N for bi-encoder
    avg_precisions_bi = {}
    print("\nAverage Precision at N using bi-encoder:")
    for N in Ns:
        avg_precision = np.mean(precisions_at_N_bi[N]) if precisions_at_N_bi[N] else 0.0
        avg_precisions_bi[N] = avg_precision
        print(f"Precision@{N}: {avg_precision:.4f}")

    ### Proceed with cross-encoder evaluation ###
    # For each candidate, get top K jobs and prepare cross-encoder inputs
    all_candidate_texts = []
    all_job_texts = []
    all_candidate_ids = []
    all_candidate_features = []
    all_job_features = []

    print("\nPreparing cross-encoder evaluation data...")
    for idx, candidate_id in tqdm_cls(enumerate(candidate_ids), total=len(candidate_ids), desc="Preparing Cross-Encoder Data"):
        sim_scores = similarities[idx]
        top_k_indices = np.argpartition(-sim_scores, K-1)[:K]
        top_k_job_texts = [job_texts[i] for i in top_k_indices]
        top_k_job_ids = [job_ids[i] for i in top_k_indices]
        candidate_text = candidate_texts[idx]
        candidate_feature = candidate_id_to_features.get(candidate_id, None)
        num_jobs = len(top_k_job_texts)
        all_candidate_texts.extend([candidate_text] * num_jobs)
        all_candidate_features.extend([candidate_feature] * num_jobs)
        all_job_texts.extend(top_k_job_texts)
        job_features = [job_id_to_features.get(job_id, None) for job_id in top_k_job_ids]
        all_job_features.extend(job_features)
        all_candidate_ids.extend([candidate_id] * num_jobs)

    # Create a dataset for cross-encoder evaluation
    eval_dataset = CrossEncoderEvalDataset(all_candidate_texts, all_job_texts)
    eval_dataloader = DataLoader(eval_dataset, batch_size=config['eval_batch_size'], shuffle=False, num_workers=config['num_workers'], pin_memory=True)

    print("\nEvaluating with cross-encoder...")
    scores = []
    model.eval()
    with torch.no_grad():
        for batch in tqdm_cls(eval_dataloader, desc="Cross-Encoder Evaluation"):
            c_texts, j_texts = batch
            inputs = tokenizer(c_texts, j_texts, max_length=config['max_length'], truncation=True, padding=True, return_tensors='pt').to(device)
            if config['use_sparse']:
                # Prepare and concatenate features
                candidate_features = torch.stack([
                    torch.tensor(cf, dtype=torch.float) if cf is not None else torch.zeros(config['candidate_feature_size'])
                    for cf in all_candidate_features
                ]).to(device)
                job_features = torch.stack([
                    torch.tensor(jf, dtype=torch.float) if jf is not None else torch.zeros(config['job_feature_size'])
                    for jf in all_job_features
                ]).to(device)
                # Concatenate candidate and job features if required
                features_tensor = torch.cat((candidate_features, job_features), dim=1)  # Shape: [batch_size, candidate_feature_size + job_feature_size]
                logits = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], features=features_tensor)
            else:
                logits = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])
            batch_scores = logits.cpu().numpy()
            scores.extend(batch_scores.tolist())

    # Collect scores per candidate
    candidate_job_scores = defaultdict(list)
    candidate_job_ids = defaultdict(list)
    for cid, jid, score in zip(all_candidate_ids, all_job_texts, scores):
        candidate_job_scores[cid].append(score)
        candidate_job_ids[cid].append(job_text_to_id[jid])

    # Compute precision at N using cross-encoder
    print("\nComputing Precision@N using cross-encoder scores...")
    precisions_at_N_cross = {N: [] for N in Ns}
    for candidate_id in tqdm_cls(candidate_ids, desc="Calculating Precision@N"):
        job_scores = candidate_job_scores[candidate_id]
        job_ids_list = candidate_job_ids[candidate_id]
        sorted_indices = np.argsort(-np.array(job_scores))
        sorted_job_ids = [job_ids_list[i] for i in sorted_indices]
        ground_truth_job_ids = candidate_to_jobs.get(candidate_id, set())
        for N in Ns:
            top_N_job_ids = sorted_job_ids[:N]
            hits = ground_truth_job_ids.intersection(top_N_job_ids)
            precision = len(hits) / N
            precisions_at_N_cross[N].append(precision)

    # Compute average precision at each N for cross-encoder
    avg_precisions = {}
    print("\nAverage Precision at N using cross-encoder:")
    for N in Ns:
        avg_precision = np.mean(precisions_at_N_cross[N]) if precisions_at_N_cross[N] else 0.0
        avg_precisions[N] = avg_precision
        print(f"Precision@{N}: {avg_precision:.4f}")

    # Log evaluation metrics to W&B or MLflow if enabled
    metrics = {f"Precision@{N}": avg_precisions[N] for N in Ns}
    metrics.update({f"BiEncoder Precision@{N}": avg_precisions_bi[N] for N in Ns})
    metrics["Epoch"] = epoch + 1

    if config.get('use_wandb', False):
        wandb.log(metrics)
    elif config.get('use_mlflow', False):
        for key, value in metrics.items():
            mlflow.log_metric(key, value, step=epoch + 1)

    return avg_precisions


def precompute_bi_encoder_negatives(bi_encoder, tokenizer, candidates, jobs, positive_matches, config):
    """
    Precompute negatives using the bi-encoder by computing similarities and selecting top negatives.
    Optimized with vectorized operations and batching.
    """
    tqdm_cls = get_tqdm(config)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    bi_encoder.to(device)
    bi_encoder.eval()

    candidate_texts = [candidate['candidate_text'] for candidate in candidates]
    candidate_ids = [candidate['candidate_id'] for candidate in candidates]
    job_texts = [job['job_text'] for job in jobs]
    job_ids = [job['job_id'] for job in jobs]

    # Compute embeddings in batches
    print("Computing candidate embeddings...")
    candidate_embeddings = compute_bi_encoder_embeddings(bi_encoder, tokenizer, candidate_texts, config)
    print("Computing job embeddings...")
    job_embeddings = compute_bi_encoder_embeddings(bi_encoder, tokenizer, job_texts, config)

    # Normalize embeddings
    candidate_embeddings = nn.functional.normalize(candidate_embeddings, p=2, dim=1)
    job_embeddings = nn.functional.normalize(job_embeddings, p=2, dim=1)

    # Move embeddings to CPU for similarity computation
    candidate_embeddings = candidate_embeddings.cpu()
    job_embeddings = job_embeddings.cpu()

    # Compute similarity matrix
    print("Computing similarity matrix...")
    similarity_matrix = torch.matmul(candidate_embeddings, job_embeddings.t()).numpy()  # Shape: [num_candidates, num_jobs]

    # Build positive matches set
    positive_pairs = defaultdict(set)
    for match in positive_matches:
        positive_pairs[match['candidate_id']].add(match['job_id'])

    M = config['M']
    use_sparse = config['use_sparse']

    # Initialize negatives dictionary
    negatives = defaultdict(dict)

    # Vectorized masking of positive pairs
    print("Masking positive pairs in similarity matrix...")
    # Create a mask matrix where positive pairs are True
    mask = np.zeros_like(similarity_matrix, dtype=bool)
    for cid, jids in positive_pairs.items():
        if cid in candidate_ids:
            cid_idx = candidate_ids.index(cid)
            jid_indices = [job_ids.index(jid) for jid in jids if jid in job_ids]
            mask[cid_idx, jid_indices] = True
    # Set similarities of positive pairs to -inf
    similarity_matrix[mask] = -np.inf

    # Get top M negatives per candidate starting from start_rank
    print("Selecting top M negatives per candidate...")
    start_rank = config.get('start_rank', 1000)
    end_rank = start_rank + M
    num_candidates, num_jobs = similarity_matrix.shape

    # Handle cases where start_rank exceeds number of jobs
    valid_start_rank = min(start_rank, num_jobs)
    valid_end_rank = min(end_rank, num_jobs)

    # Use argpartition for efficient top-k selection
    top_m_indices = np.argpartition(-similarity_matrix, valid_end_rank - 1, axis=1)[:, start_rank:valid_end_rank]  # Shape: [num_candidates, M]

    # Retrieve job_ids and job_texts based on indices
    top_m_job_ids = np.take(job_ids, top_m_indices, axis=0)  # Shape: [num_candidates, M]
    top_m_job_texts = np.take(job_texts, top_m_indices, axis=0)  # Shape: [num_candidates, M]

    # Populate the negatives dictionary
    for idx, cid in tqdm_cls(enumerate(candidate_ids), total=len(candidate_ids), desc="Populating negatives"):
        neg_ids = top_m_job_ids[idx].tolist()
        neg_texts = top_m_job_texts[idx].tolist()
        negatives[cid]['job_ids'] = neg_ids
        negatives[cid]['job_texts'] = neg_texts

        if use_sparse:
            neg_features = [jobs[job_ids.index(jid)].get('job_features', None) for jid in neg_ids]
            negatives[cid]['job_features'] = neg_features

    return negatives


# Additional helper functions can be added here if needed


