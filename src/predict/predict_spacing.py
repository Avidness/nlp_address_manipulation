import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from datasets import Dataset
from pathlib import Path
import torch

data_dir = Path(__file__).resolve().parent.parent.parent / 'data'
data_df = pd.read_csv(data_dir / 'addr_clean_manual.csv')

model_dir = Path(__file__).resolve().parent.parent.parent / 'models'
model_path = model_dir / 'transform_spacing'
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Tokenize the test data
def preprocess_test_function(examples):
    inputs = examples['address']
    model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length", return_tensors="pt")
    return model_inputs

test_dataset = Dataset.from_pandas(data_df)
data_df['address'] = data_df['address'].astype(str)
tokenized_test_datasets = test_dataset.map(preprocess_test_function, batched=True)

# Use model.generate to predict the cleaned addresses in batches
def generate_predictions(dataset, batch_size=100):
    address_list = dataset['address'].astype(str).tolist()
    all_predictions = []
    total_batches = (len(address_list) + batch_size - 1) // batch_size  # Calculate the total number of batches
    
    with torch.no_grad():
        for i in range(total_batches):
            start_idx = i * batch_size
            batch_addresses = address_list[start_idx:start_idx + batch_size]
            inputs = tokenizer(batch_addresses, return_tensors='pt', padding=True, truncation=True)
            outputs = model.generate(**inputs)
            decoded_preds = tokenizer.batch_decode(outputs, skip_special_tokens=True)
            all_predictions.extend(decoded_preds)
            print(f'Batch {i + 1} of {total_batches} completed', end="\r", flush=True)
    
    print()  # Move to the next line after finishing all batches
    return all_predictions


# Predict the cleaned addresses
predictions = generate_predictions(data_df)

# Add the cleaned addresses to the test DataFrame
data_df['address_cleaned'] = predictions

data_df = data_df[['address', 'address_cleaned']]
data_df.to_csv(data_dir / 'predictions_spacing.csv', index=False)