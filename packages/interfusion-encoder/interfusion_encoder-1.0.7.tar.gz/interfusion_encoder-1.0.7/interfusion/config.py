# interfusion/config.py

def get_default_config():
    # Default configuration dictionary
    config = {
        'random_seed': 66,
        'max_length': 32,
        'use_sparse': False,  # Flag to enable or disable the use of sparse features

        # Logging and Tracking
        'use_wandb': True,     # Set to True to enable W&B, False to disable
        'use_mlflow': False,   # Set to True to enable MLflow, False to disable
        'wandb_project': 'interfusion_project',  # W&B project name
        'wandb_run_name': 'interfusion_run',      # W&B run name

        # Model Specifications
        'bi_encoder_model_name': 'bert-base-uncased',    # Bi-encoder model name
        'cross_encoder_model_name': 'bert-base-uncased', # Cross-encoder model name

        # Training Hyperparameters
        'learning_rate': 2e-5,           # Maximum learning rate
        'initial_learning_rate': 2e-8,   # Initial learning rate at epoch 0
        'num_epochs': 10,                 # Total number of training epochs
        'temperature': 1.0,               # Temperature parameter for softmax

        # Batch Sizes
        'train_batch_size': 32,           # Number of training samples per batch
        'eval_batch_size': 64,            # Number of evaluation samples per batch
        'negative_batch_size': 256,       # Number of negative samples processed in each batch when generating hard negatives

        # Data Loading
        'num_workers': 4,                 # Number of worker threads for data loading

        # Negative Sampling Parameters
        'M': 250,                          # Number of negatives to precompute per candidate
        'N': 10,                           # Number of hard negatives and random negatives per candidate (each)
        'start_rank': 1000,                # Rank from which to start selecting negative samples based on similarity scores
        'hard_negative_sampling_frequency': 2,  # Frequency (in epochs) at which hard negatives are regenerated

        # Evaluation Parameters
        'eval_Ns': [1, 5, 10],             # List of N values for Precision@N
        'eval_K': 50,                      # Number of top jobs to retrieve using the bi-encoder for cross-encoder evaluation
        'eval_epoch': 1,                   # Frequency (in epochs) at which the model is evaluated

        # Progress Visualization
        'use_tqdm': True,                  # Set to True to enable tqdm progress bars, False to disable
        'tqdm_type': 'standard',           # Options: 'standard', 'notebook'

        # Model Saving
        'save_dir': 'saved_models',        # Directory to save model checkpoints

        # Training Continuation
        'continue_training': False,        # Set to True to load saved model and continue training
        'saved_model_path': '',             # Path to the saved model

        # Deprecated or Legacy Parameters
        'bi_encoder_batch_size': 64,       # Deprecated: No longer used in optimized trainer.py
        # It's recommended to remove this parameter if it's no longer utilized elsewhere in your codebase.
    }
    return config


