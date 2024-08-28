import pandas as pd
import re
from pathlib import Path
from src.utils.common import add_missing_spaces

data_dir = Path(__file__).resolve().parent.parent.parent / 'data'
addresses_df = pd.read_csv(data_dir / 'addr_clean.csv')

# we don't need the country for this part
addresses_df = addresses_df.drop(columns=['country'])

# remove dups and empty
addresses_df = addresses_df.drop_duplicates(subset=['address'])
addresses_df = addresses_df.dropna(subset=['address'])

addresses_df = addresses_df[addresses_df['address'].str.contains(' ')]

# create a clean col (with spacing) and a dirty col (without spacing)
addresses_df = addresses_df.rename(columns={'address': 'address_clean'})
addresses_df['address_dirty'] = addresses_df['address_clean'].str.replace(' ', '')

# additional tweaking to improve the "clean" col
addresses_df['address_clean'] = addresses_df['address_clean'].apply(add_missing_spaces)

def has_long_continuous_string(address):
    return bool(re.search(r'\S{16,}', address))

# remove records where there is a continuous string longer than 15 characters
addresses_df = addresses_df[~addresses_df['address_clean'].apply(has_long_continuous_string)]

# Store the results in a new CSV file
addresses_df.to_csv(data_dir / 'addr_train_spacing.csv', index=False)