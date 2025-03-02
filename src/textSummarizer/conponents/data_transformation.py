import os
from textSummarizer.logging import logger
from transformers import AutoTokenizer
from datasets import load_from_disk
from textSummarizer.entity import DataTransformationConfig

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name)

    def convert_examples_to_features(self, example_batch):
        input_encodings = self.tokenizer(example_batch['dialogue'], max_length=1024, truncation=True)
        
        with self.tokenizer.as_target_tokenizer():
            target_encodings = self.tokenizer(example_batch['summary'], max_length=128, truncation=True)
            
        return {
            'input_ids': input_encodings['input_ids'],
            'attention_mask': input_encodings['attention_mask'],
            'labels': target_encodings['input_ids']
        }

    def convert(self):
        dataset_path = os.path.abspath("artifacts/data_ingestion/samsum_dataset")

        logger.info(f"Loading dataset from disk at {dataset_path}...")

        # ✅ Step 1: Debugging print statements
        print(f"Resolved dataset path: {dataset_path}")
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset directory not found: {dataset_path}")
        
        # ✅ Step 2: Ensure path is a valid string
        dataset_path = str(dataset_path)  # Explicitly convert to string
        print(f"Final dataset path: {dataset_path}")

        try:
            dataset_samsum = load_from_disk(dataset_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load dataset: {e}")

        logger.info("Tokenizing dataset...")
        dataset_samsum_pt = dataset_samsum.map(self.convert_examples_to_features, batched=True)

        save_path = os.path.join(self.config.root_dir, "samsum_dataset")
        dataset_samsum_pt.save_to_disk(save_path)

        logger.info(f"Data transformation complete! Tokenized dataset saved at {save_path}")