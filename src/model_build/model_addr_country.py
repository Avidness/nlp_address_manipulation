import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
from pathlib import Path
import joblib

# Define paths
data_dir = Path(__file__).resolve().parent.parent.parent / 'data'
model_dir = Path(__file__).resolve().parent.parent.parent / 'models'

# Load datasets
synthetic_df = pd.read_csv(data_dir / 'synthetic_addr_country_pairs.csv')
real_df = pd.read_csv(data_dir / 'addr_chopped.csv')

# Combine datasets
synthetic_df = synthetic_df.rename(columns={'address': 'addr_chopped'})
df = pd.concat([synthetic_df, real_df])

# Filter records with non-empty country values
df_with_country = df.dropna(subset=['country_iso']).dropna(subset=['addr_chopped'])

# Remove entries where country_iso has fewer than 5 examples
country_counts = df_with_country['country_iso'].value_counts()
df_with_country = df_with_country[df_with_country['country_iso'].isin(country_counts[country_counts >= 5].index)]

# Split data into features and target
X = df_with_country['addr_chopped']
y = df_with_country['country_iso']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize text data
vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Apply SMOTE to handle class imbalance
smote = SMOTE(random_state=42, k_neighbors=1)
X_train_tfidf_res, y_train_res = smote.fit_resample(X_train_tfidf, y_train)

# Train Logistic Regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf_res, y_train_res)

# Predict on test data
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Save the model and vectorizer
joblib.dump(model, model_dir / 'addr_country_predict.joblib')
joblib.dump(vectorizer, model_dir / 'tfidf_vectorizer.joblib')
print('Cached model')

# Compile and store results
results_df = pd.DataFrame({
    'address': X_test,
    'actual_country': y_test,
    'predicted_country': y_pred
})

# Store false predictions for later analysis
false_predictions_df = results_df[results_df['actual_country'] != results_df['predicted_country']]
false_predictions_df.to_csv(data_dir / 'preds_failures.csv', index=False)
print('Stored false positives in pred_failures.csv')
