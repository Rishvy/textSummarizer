from datasets import load_from_disk

# Load dataset from the directory
dataset = load_from_disk("/Users/user/Downloads/Text-Summarization-NLP-Project-main/artifacts/data_ingestion/samsum_dataset")

# Save train, validation, and test sets as CSV
dataset["train"].to_csv("/Users/user/Downloads/Text-Summarization-NLP-Project-main/artifacts/data_ingestion/samsum_dataset/samsum-train.csv", index=False)
dataset["validation"].to_csv("/Users/user/Downloads/Text-Summarization-NLP-Project-main/artifacts/data_ingestion/samsum_dataset/samsum-validation.csv", index=False)
dataset["test"].to_csv("/Users/user/Downloads/Text-Summarization-NLP-Project-main/artifacts/data_ingestion/samsum_dataset/samsum-test.csv", index=False)

print("Dataset successfully converted to CSV!")