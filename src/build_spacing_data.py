import pandas as pd
import re
from pathlib import Path

data_dir = Path(__file__).resolve().parent.parent / 'data'
addresses_df = pd.read_csv(data_dir / 'addr_clean.csv')

# we don't need the country for this part
addresses_df = addresses_df.drop(columns=['country'])

# remove dups and empty
addresses_df = addresses_df.drop_duplicates(subset=['address'])
addresses_df = addresses_df.dropna(subset=['address'])

# TODO: remove addresses that are a single word, set a limit for length of words

# create a clean col (with spacing) and a dirty col (without spacing)
addresses_df = addresses_df.rename(columns={'address': 'address_clean'})
addresses_df['address_dirty'] = addresses_df['address_clean'].str.replace(' ', '')

def add_missing_spaces(text):
    # Add a space between a number followed by a letter
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
    # Add a space between a letter followed by a number
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    return text

# additional tweaking to improve the "clean" col
addresses_df['address_clean'] = addresses_df['address_clean'].apply(add_missing_spaces)

# Store the results in a new CSV file
addresses_df.to_csv(data_dir / 'addr_train_spacing.csv', index=False)