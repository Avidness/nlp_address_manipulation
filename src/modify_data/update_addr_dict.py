import pickle
from pathlib import Path
import csv

# Define special words
special_words = ['deli', 'istanbul', 'tokyo', 'strasse', 'strase', 'straße', 'turkey', 'turkiye', 'moscow', 'building', 'china', 'hong','kong','unit','flat','plaza','dubai','munchen', 'city', 'room', 'province', 'kowloon', 'district']

# Load the original pickle file
data_dir = Path(__file__).resolve().parent.parent / 'data'
with open(data_dir / 'addr_word_dict.pkl', 'rb') as f:
    data_dict = pickle.load(f)

# Function to split a word based on delimiters
def split_by_delimiters(word):
    delimiters = ['\\', '-', ',', ';', '(', ')', '.', '?', '\'', '/', '"', '#']
    split_words = []
    current_word = []
    for char in word:
        if char in delimiters:
            if current_word:
                split_words.append(''.join(current_word))
                current_word = []
        else:
            current_word.append(char)
    if current_word:
        split_words.append(''.join(current_word))
    return split_words

# Function to split a word based on special words
def split_by_special_words(word, special_words):
    split_words = []
    i = 0
    while i < len(word):
        found_special = False
        for special_word in special_words:
            if word[i:i+len(special_word)].lower() == special_word:
                if i > 0:
                    split_words.append(word[:i])
                split_words.append(word[i:i+len(special_word)])
                word = word[i+len(special_word):]
                i = 0
                found_special = True
                break
        if not found_special:
            i += 1
    if word:
        split_words.append(word)
    return split_words

# Helper function to check if a string contains any numeric characters
def contains_numeric(key):
    return any(char.isdigit() for char in key)

# Process the dictionary
updated_dict = {}
for key, value in data_dict.items():
    # Convert the key to lowercase
    key = key.lower()
    
    # Split the key by the specified delimiters
    split_keys = split_by_delimiters(key)
    
    for split_key in split_keys:
        # Further split by special words if any are found
        further_split_keys = split_by_special_words(split_key, special_words)
        
        for new_key in further_split_keys:
            # Check if the key contains any numeric characters
            if len(new_key) > 1 and not contains_numeric(new_key):
                if new_key not in updated_dict:
                    updated_dict[new_key] = value
                else:
                    updated_dict[new_key] += value

# Save the cleaned dictionary as a CSV file
csv_file_path = data_dir / 'addr_word_dict_cleaned.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Key', 'Value'])
    for key, value in updated_dict.items():
        writer.writerow([key, value])

print(f"Processed dictionary saved to 'addr_word_dict_cleaned.csv'.")

# Save the modified dictionary to a separate .pkl file
with open(data_dir / 'addr_word_dict_cleaned.pkl', 'wb') as f:
    pickle.dump(updated_dict, f)
