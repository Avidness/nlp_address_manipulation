from pathlib import Path
import pandas as pd
from src.utils.localLLM import llama_get_country
import time

# load data\
data_dir = Path(__file__).resolve().parent.parent.parent / 'data'
df = pd.read_csv(data_dir / 'addr_clean.csv')
df = df.dropna(subset=['address'])

start_time = time.time()
df[['country_code', 'certainty']] = df['address'].apply(lambda x: pd.Series(llama_get_country(x)))

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

df.to_csv(data_dir / 'addr_with_country_llm.csv', index=False)
