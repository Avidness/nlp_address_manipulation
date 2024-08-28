from pathlib import Path
import pandas as pd
from utils.common import df_to_dictionary, add_missing_spaces
import time

# load data\
data_dir = Path(__file__).resolve().parent.parent.parent / 'data'
df = pd.read_csv(data_dir / 'addr_clean.csv')
df = df.dropna(subset=['address'])

df['address'] = df['address'].apply(add_missing_spaces)

start_time = time.time()
word_dict = df_to_dictionary(df, 'address', 15)
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

import pickle
with open(data_dir / 'addr_word_dict.pkl', 'wb') as f:
    pickle.dump(word_dict, f)
