import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments
from datasets import Dataset
from sklearn.model_selection import train_test_split
import os
from pathlib import Path

data_dir = Path(__file__).resolve().parent.parent / 'data'
data_df = pd.read_csv(data_dir / 'addr_train_spacing.csv')

train_df, eval_df = train_test_split(data_df, test_size=0.1, random_state=42)
train_dataset = Dataset.from_pandas(train_df)
eval_dataset = Dataset.from_pandas(eval_df)

model_name = 't5-small'
tokenizer = AutoTokenizer.from_pretrained(model_name)

model_dir = Path(__file__).resolve().parent.parent / 'models'
model_path = model_dir / 'transform_spacing'

if os.path.exists(model_path):
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
else:
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Tokenize the input data
    def preprocess_function(examples):
        inputs = examples['address_dirty']
        targets = examples['address_clean']
        model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")

        # Setup the tokenizer for targets
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length")

        # Convert lists to PyTorch tensors for indexing
        labels_ids = torch.tensor(labels["input_ids"])
        decoder_input_ids = labels_ids.clone()

        # Shift the decoder_input_ids to the right
        decoder_input_ids[:, 1:] = labels_ids[:, :-1]
        decoder_input_ids[:, 0] = tokenizer.pad_token_id

        model_inputs["labels"] = labels_ids.tolist()
        model_inputs["decoder_input_ids"] = decoder_input_ids.tolist()

        return model_inputs

    tokenized_train_datasets = train_dataset.map(preprocess_function, batched=True)
    tokenized_eval_datasets = eval_dataset.map(preprocess_function, batched=True)

    # Define training arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir='./results',
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        num_train_epochs=3,
        save_steps=10_000,
        save_total_limit=2,
    )

    # Initialize the Trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train_datasets,
        eval_dataset=tokenized_eval_datasets,
        tokenizer=tokenizer,
    )

    # Train the model
    trainer.train()

    # Save the trained model
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)

# Test data examples
test_data = [
    "000000GUANGDONGSHUNDEFOSHANRONGGUICHUANG",
    "00695WARSZAWAUL NOWOGRODZKA NR50LOK515",
    "01001ZILINABRATISLAVASKA CESTA60",
    "01189DRESDENCUNNERSDORFER STR 25",
    "1STAVENNYC10019",
    "00000 SOUTH SUDAN JUBA PO BOX 440 JEBEL KUJUR",
    "00160HELSINKILUOTSIKATU3",
    "00144ROMAVIA MAROCCO56",
    "00700COLOMBOANANDA COOMARASWAMY MAWATHA51"
]

# Create a DataFrame from the test data
test_df = pd.DataFrame(test_data, columns=['address'])

# Tokenize the test data
def preprocess_test_function(examples):
    inputs = examples['address']
    model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length", return_tensors="pt")
    return model_inputs

test_dataset = Dataset.from_pandas(test_df)
test_df['address'] = test_df['address'].astype(str)
tokenized_test_datasets = test_dataset.map(preprocess_test_function, batched=True)

# Use model.generate to predict the cleaned addresses
def generate_predictions(dataset):
    address_list = dataset['address'].astype(str).tolist()
    inputs = tokenizer(address_list, return_tensors='pt', padding=True, truncation=True)
    outputs = model.generate(**inputs)
    decoded_preds = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return decoded_preds

# Predict the cleaned addresses
predictions = generate_predictions(test_df)

# Add the cleaned addresses to the test DataFrame
test_df['address_cleaned'] = predictions

# Output the results
print(test_df[['address', 'address_cleaned']])
