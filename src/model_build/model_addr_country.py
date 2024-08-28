import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from pathlib import Path
import joblib

# List of countries
countries = [
    'India','China','United States','Indonesia','Pakistan','Nigeria','Brazil','Bangladesh','Russia',
    'Ethiopia','Mexico','Japan','Egypt','Philippines','DR Congo','Vietnam','Iran','Turkey','Germany',
    'Thailand','United Kingdom','Tanzania','France','South Africa','Italy','Kenya','Myanmar','Colombia',
    'South Korea','Sudan','Uganda','Spain','Algeria','Iraq','Argentina','Afghanistan','Yemen','Canada',
    'Poland','Morocco','Angola','Ukraine','Uzbekistan','Malaysia','Mozambique','Ghana','Peru','Saudi Arabia',
    'Madagascar','Côte d\'Ivoire','Nepal','Cameroon','Venezuela','Niger','Australia','North Korea','Syria',
    'Mali','Burkina Faso','Sri Lanka','Malawi','Zambia','Kazakhstan','Chad','Chile','Romania','Somalia',
    'Senegal','Guatemala','Netherlands','Ecuador','Cambodia','Zimbabwe','Guinea','Benin','Rwanda','Burundi',
    'Bolivia','Tunisia','South Sudan','Haiti','Belgium','Jordan','Dominican Republic','United Arab Emirates',
    'Cuba','Honduras','Czech Republic (Czechia)','Sweden','Tajikistan','Papua New Guinea','Portugal',
    'Azerbaijan','Greece','Hungary','Togo','Israel','Austria','Belarus','Switzerland','Sierra Leone',
    'Laos','Turkmenistan','Libya','Kyrgyzstan','Paraguay','Nicaragua','Bulgaria','Serbia','El Salvador',
    'Congo','Denmark','Singapore','Lebanon','Finland','Liberia','Norway','Slovakia','State of Palestine',
    'Central African Republic','Oman','Ireland','New Zealand','Mauritania','Costa Rica','Kuwait','Panama',
    'Croatia','Georgia','Eritrea','Mongolia','Uruguay','Bosnia and Herzegovina','Qatar','Moldova','Namibia',
    'Armenia','Lithuania','Jamaica','Albania','Gambia','Gabon','Botswana','Lesotho','Guinea-Bissau',
    'Slovenia','Equatorial Guinea','Latvia','North Macedonia','Bahrain','Trinidad and Tobago','Timor-Leste',
    'Estonia','Cyprus','Mauritius','Eswatini','Djibouti','Fiji','Comoros','Guyana','Solomon Islands','Bhutan',
    'Luxembourg','Montenegro','Suriname','Malta','Maldives','Micronesia','Cabo Verde','Brunei','Belize',
    'Bahamas','Iceland','Vanuatu','Barbados','Sao Tome & Principe','Samoa','Saint Lucia','Kiribati','Seychelles',
    'Grenada','Tonga','St. Vincent & Grenadines','Antigua and Barbuda','Andorra','Dominica','Saint Kitts & Nevis',
    'Liechtenstein','Monaco','Marshall Islands','San Marino','Palau','Nauru','Tuvalu','Holy See'
]

data_dir = Path(__file__).resolve().parent.parent / 'data'
df = pd.read_csv(data_dir / 'addr_chopped.csv')
df['text'] = df['addr_chopped'].str.replace(r'\s+', ' ', regex=True)

# Get recs with a non-empty country value
df_with_country = df.dropna(subset=['country']).dropna(subset=['addr_chopped'])

# Add new rows to df_with_country from the countries list
for country in countries:
    new_row = pd.DataFrame({'addr_chopped': [country.lower()], 'country': [country.lower()]})
    df_with_country = pd.concat([df_with_country, new_row], ignore_index=True)

# Split
X = df_with_country['addr_chopped']
y = df_with_country['country']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# Predict the country field on test data
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Store the model
model_dir = Path(__file__).resolve().parent.parent / 'models'
joblib.dump(model, model_dir / 'addr_country_predict.joblib')
joblib.dump(vectorizer, model_dir / 'tfidf_vectorizer.joblib')
print('Cached model')

# Compile results
results_df = pd.DataFrame({
    'address': X_test,
    'actual_country': y_test,
    'predicted_country': y_pred
})

# Store false predictions for later analysis
false_predictions_df = results_df[results_df['actual_country'] != results_df['predicted_country']]
false_predictions_df.to_csv(data_dir / 'preds_failures.csv', index=False)
print('Stored false positives in pred_failures.csv')
