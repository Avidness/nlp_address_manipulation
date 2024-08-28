import nltk
from nltk.corpus import brown
import spacy
import pandas as pd
import pickle
from pathlib import Path
import re

# Download the words dataset if you haven't already
nltk.download('brown')

# Initialize the word lists from both nltk and spaCy
nltk_words = set(brown.words())
nlp = spacy.blank("en")
spacy_words = set(nlp.vocab.strings)

# Load the dictionary from the .pkl file
data_dir = Path(__file__).resolve().parent.parent.parent / 'data'
with open(data_dir / 'addr_word_dict_cleaned.pkl', 'rb') as file:
    my_dict = pickle.load(file)

# Create a new dictionary with lowercase keys
updated_dict = {key.lower(): value for key, value in my_dict.items()}

# Optionally, replace the original dictionary with the updated one
my_dict = updated_dict

# Combine both dictionaries
combined_word_list = my_dict

def add_spaces_greedy(text, word_dict):
    i = 0
    result = []
    text = text.lower()

    while i < len(text):
        # Initialize variables for the longest word found
        longest_word = None
        longest_len = 0
        
        # Try to find the longest word in the dictionary that matches the current substring
        for j in range(i + 1, len(text) + 1):
            word = text[i:j]
            if word in word_dict and len(word) > longest_len:
                longest_word = word
                longest_len = len(word)
        
        # If a word was found, add it to the result
        if longest_word:
            result.append(longest_word)
            i += longest_len
        else:
            # If no word is found, move one character forward and add it as-is
            result.append(text[i])
            i += 1

    # Rejoin numeric sequences
    processed_text = " ".join(result)
    processed_text = re.sub(r'(\d)\s+(?=\d)', r'\1', processed_text)
    
    return processed_text

def remove_unwanted_words_and_numbers(text):
    # List of unwanted words
    unwanted_words = {
        'avenue', 'rd', 'road', 'blvd', 'boulevard', 'st', 'street', 'building', 'buildings'
    }
    
    # Remove unwanted words
    words = text.split()
    words = [word for word in words if word not in unwanted_words]
    
    # Remove numbers
    words = [word for word in words if not word.isdigit()]
    
    return " ".join(words)

data_dir = Path(__file__).resolve().parent.parent.parent / 'data'
df = pd.read_csv(data_dir / 'addr_clean.csv')

df = df[df['address'].notna() & df['address'].str.strip().astype(bool)]

# Apply the transformations
df['addr_chopped'] = df['address'].apply(lambda s: add_spaces_greedy(s, combined_word_list))
df['addr_chopped'] = df['addr_chopped'].apply(remove_unwanted_words_and_numbers)
df['addr_chopped'] = df['addr_chopped'].str.replace(r'\s+', ' ', regex=True)

df.to_csv(data_dir / 'addr_chopped.csv', index=False)
