import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments
from datasets import Dataset
from sklearn.model_selection import train_test_split
from pathlib import Path

data_dir = Path(__file__).resolve().parent.parent.parent / 'data'
data_df = pd.read_csv(data_dir / 'addr_train_spacing.csv')

train_df, eval_df = train_test_split(data_df, test_size=0.1, random_state=42)
train_dataset = Dataset.from_pandas(train_df)
eval_dataset = Dataset.from_pandas(eval_df)

model_name = 't5-small'
tokenizer = AutoTokenizer.from_pretrained(model_name)

model_dir = Path(__file__).resolve().parent.parent.parent / 'models'
model_path = model_dir / 'transform_spacing'


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
    output_dir=model_dir / 'spacing_model_results',
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
