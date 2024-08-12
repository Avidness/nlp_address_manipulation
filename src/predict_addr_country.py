
import pandas as pd
from pathlib import Path
import joblib

data_dir = Path(__file__).resolve().parent.parent / 'data'
df = pd.read_csv(data_dir / 'addr_clean.csv')

# records where the country field is empty
df = df.dropna(subset=['address'])
df_empty_country = df[df['country'].isna()]

# load the model
model_dir = Path(__file__).resolve().parent.parent / 'models'
model = joblib.load(model_dir / 'addr_country_predict.joblib')
vectorizer = joblib.load(model_dir / 'tfidf_vectorizer.joblib')

# vectorize
X_empty_country_tfidf = vectorizer.transform(df_empty_country['address'])

# predict
predicted_countries = model.predict(X_empty_country_tfidf)

# add the predictions to the original df
df_empty_country['predicted_country'] = predicted_countries

# store as a csv for later analysis
df_empty_country.to_csv(data_dir / 'predictions_attempted.csv', index=False)