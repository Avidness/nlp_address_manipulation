import pandas as pd
from pathlib import Path

data_dir = Path(__file__).resolve().parent.parent / 'data'
df = pd.read_csv(data_dir / 'addr_raw.csv')

# Specific parse/cleanse for this data 
def clean_addr(record):
    parts = [part.strip() for part in str(record).split(',')]
    cleaned_parts = [part for part in parts if part and part.lower() != 'none' and part.lower() != 'nan' and part.lower() != 'nannan']
    return ' '.join(cleaned_parts) if cleaned_parts else None

df['address'] = df['address'].apply(clean_addr)

# dump invalid stuff
invalid_addresses = ["", None, "NaN", "NaNNaN", "na", "n/a", "nan", ",,,,", "None", 'none']
df_cleaned = df[~df['address'].isin(invalid_addresses)].dropna(subset=['address'])

print("# w/ country:", df_cleaned['country'].notnull().sum())
print("# w/o country:", df_cleaned['country'].isnull().sum())

df.to_csv(data_dir / 'addr_clean.csv', index=False)