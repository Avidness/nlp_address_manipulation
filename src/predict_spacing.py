import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from datasets import Dataset
from pathlib import Path

model_dir = Path(__file__).resolve().parent.parent / 'models'
model_path = model_dir / 'transform_spacing'
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Test data examples
test_data = [
    "000000GUANGDONGSHUNDEFOSHANRONGGUICHUANG",
    "00695WARSZAWAUL NOWOGRODZKA NR50LOK515",
    "01001ZILINABRATISLAVASKA CESTA60",
    "01189DRESDENCUNNERSDORFER STR 25",
    "1STAVENYC10019",
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
