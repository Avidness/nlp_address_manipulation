import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from pathlib import Path
import joblib

data_dir = Path(__file__).resolve().parent.parent / 'data'
df = pd.read_csv(data_dir / 'addr_clean.csv')

# get recs with a non empy country value
df_with_country = df.dropna(subset=['country']).dropna(subset=['address'])

# split
X = df_with_country['address']
y = df_with_country['country']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# vectorize
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# train
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# predict the country field on test data
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# store the model
model_dir = Path(__file__).resolve().parent.parent / 'models'
joblib.dump(model, model_dir / 'addr_country_predict.joblib')
joblib.dump(vectorizer, model_dir / 'tfidf_vectorizer.joblib')
print('Cached model')

# compile results
results_df = pd.DataFrame({
    'address': X_test,
    'actual_country': y_test,
    'predicted_country': y_pred
})

# store false predictions for later analysis
false_predictions_df = results_df[results_df['actual_country'] != results_df['predicted_country']]
false_predictions_df.to_csv(data_dir / 'prediction_failures.csv', index=False)
print('Stored false positives in prediction_failures.csv')