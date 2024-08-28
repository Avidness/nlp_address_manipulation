import pandas as pd
from pathlib import Path

# List of countries
countries = [
    'India', 'China', 'United States', 'Indonesia', 'Pakistan', 'Nigeria', 'Brazil', 'Bangladesh', 'Russia',
    'Ethiopia', 'Mexico', 'Japan', 'Egypt', 'Philippines', 'DR Congo', 'Vietnam', 'Iran', 'Turkey', 'Germany',
    'Thailand', 'United Kingdom', 'Tanzania', 'France', 'South Africa', 'Italy', 'Kenya', 'Myanmar', 'Colombia',
    'South Korea', 'Sudan', 'Uganda', 'Spain', 'Algeria', 'Iraq', 'Argentina', 'Afghanistan', 'Yemen', 'Canada',
    'Poland', 'Morocco', 'Angola', 'Ukraine', 'Uzbekistan', 'Malaysia', 'Mozambique', 'Ghana', 'Peru', 'Saudi Arabia',
    'Madagascar', 'Côte d\'Ivoire', 'Nepal', 'Cameroon', 'Venezuela', 'Niger', 'Australia', 'North Korea', 'Syria',
    'Mali', 'Burkina Faso', 'Sri Lanka', 'Malawi', 'Zambia', 'Kazakhstan', 'Chad', 'Chile', 'Romania', 'Somalia',
    'Senegal', 'Guatemala', 'Netherlands', 'Ecuador', 'Cambodia', 'Zimbabwe', 'Guinea', 'Benin', 'Rwanda', 'Burundi',
    'Bolivia', 'Tunisia', 'South Sudan', 'Haiti', 'Belgium', 'Jordan', 'Dominican Republic', 'United Arab Emirates',
    'Cuba', 'Honduras', 'Czech Republic (Czechia)', 'Sweden', 'Tajikistan', 'Papua New Guinea', 'Portugal',
    'Azerbaijan', 'Greece', 'Hungary', 'Togo', 'Israel', 'Austria', 'Belarus', 'Switzerland', 'Sierra Leone',
    'Laos', 'Turkmenistan', 'Libya', 'Kyrgyzstan', 'Paraguay', 'Nicaragua', 'Bulgaria', 'Serbia', 'El Salvador',
    'Congo', 'Denmark', 'Singapore', 'Lebanon', 'Finland', 'Liberia', 'Norway', 'Slovakia', 'State of Palestine',
    'Central African Republic', 'Oman', 'Ireland', 'New Zealand', 'Mauritania', 'Costa Rica', 'Kuwait', 'Panama',
    'Croatia', 'Georgia', 'Eritrea', 'Mongolia', 'Uruguay', 'Bosnia and Herzegovina', 'Qatar', 'Moldova', 'Namibia',
    'Armenia', 'Lithuania', 'Jamaica', 'Albania', 'Gambia', 'Gabon', 'Botswana', 'Lesotho', 'Guinea-Bissau',
    'Slovenia', 'Equatorial Guinea', 'Latvia', 'North Macedonia', 'Bahrain', 'Trinidad and Tobago', 'Timor-Leste',
    'Estonia', 'Cyprus', 'Mauritius', 'Eswatini', 'Djibouti', 'Fiji', 'Comoros', 'Guyana', 'Solomon Islands', 'Bhutan',
    'Luxembourg', 'Montenegro', 'Suriname', 'Malta', 'Maldives', 'Micronesia', 'Cabo Verde', 'Brunei', 'Belize',
    'Bahamas', 'Iceland', 'Vanuatu', 'Barbados', 'Sao Tome & Principe', 'Samoa', 'Saint Lucia', 'Kiribati', 'Seychelles',
    'Grenada', 'Tonga', 'St. Vincent & Grenadines', 'Antigua and Barbuda', 'Andorra', 'Dominica', 'Saint Kitts & Nevis',
    'Liechtenstein', 'Monaco', 'Marshall Islands', 'San Marino', 'Palau', 'Nauru', 'Tuvalu', 'Holy See'
]

# Load the worldcities.csv
data_dir = Path(__file__).resolve().parent.parent.parent / 'data'
df = pd.read_csv(data_dir / 'worldcities.csv')

# Prepare an empty DataFrame for the synthetic data
columns = ['address', 'country']
synthetic_df = pd.DataFrame(columns=columns)

# Add city / country pairs
city_country = df[['city', 'country']].copy()
city_country.columns = columns
synthetic_df = pd.concat([synthetic_df, city_country])

# Add admin_name / country pairs
admin_country = df[['admin_name', 'country']].copy()
admin_country.columns = columns
synthetic_df = pd.concat([synthetic_df, admin_country])

# Add city_ascii / country pairs
city_ascii_country = df[['city_ascii', 'country']].copy()
city_ascii_country.columns = columns
synthetic_df = pd.concat([synthetic_df, city_ascii_country])

# Add countries array to the synthetic_df
for country in countries:
    new_row = pd.DataFrame({'address': [country], 'country': [country]})
    synthetic_df = pd.concat([synthetic_df, new_row], ignore_index=True)

# Lowercase all entries
synthetic_df = synthetic_df.apply(lambda x: x.str.lower())

# Save the DataFrame to a CSV file
output_path = data_dir / 'synthetic_addr_country_pairs.csv'
synthetic_df.to_csv(output_path, index=False)

print(f"Saved synthetic address-country pairs to {output_path}")
