import re

def add_missing_spaces(text):
    # Add a space between a number followed by a letter
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
    # Add a space between a letter followed by a number
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    # Remove newlines and replace with spaces
    text = text.replace('\n', ' ')
    return text

def add_country_iso_column(df):
  country_iso_map = {
      'Japan': 'JP', 'Indonesia': 'ID', 'India': 'IN', 'China': 'CN', 'Philippines': 'PH', 
      'Brazil': 'BR', 'Korea, South': 'KR', 'Mexico': 'MX', 'Egypt': 'EG', 'United States': 'US', 
      'Bangladesh': 'BD', 'Thailand': 'TH', 'Russia': 'RU', 'Argentina': 'AR', 'Nigeria': 'NG', 
      'Turkey': 'TR', 'Pakistan': 'PK', 'Vietnam': 'VN', 'Iran': 'IR', 'Congo (Kinshasa)': 'CD', 
      'United Kingdom': 'GB', 'France': 'FR', 'Peru': 'PE', 'Angola': 'AO', 'Malaysia': 'MY', 
      'South Africa': 'ZA', 'Colombia': 'CO', 'Tanzania': 'TZ', 'Sudan': 'SD', 'Hong Kong': 'HK', 
      'Saudi Arabia': 'SA', 'Chile': 'CL', 'Spain': 'ES', 'Iraq': 'IQ', 'Singapore': 'SG', 
      'Cameroon': 'CM', 'Canada': 'CA', 'Kenya': 'KE', 'Burma': 'MM', 'Australia': 'AU', 
      'Côte d’Ivoire': 'CI', 'Germany': 'DE', 'Afghanistan': 'AF', 'Mali': 'ML', 'Jordan': 'JO', 
      'Morocco': 'MA', 'Ghana': 'GH', 'Algeria': 'DZ', 'United Arab Emirates': 'AE', 'Bolivia': 'BO', 
      'Greece': 'GR', 'Ethiopia': 'ET', 'Taiwan': 'TW', 'Guatemala': 'GT', 'Kuwait': 'KW', 
      'Hungary': 'HU', 'Yemen': 'YE', 'Uzbekistan': 'UZ', 'Ukraine': 'UA', 'Korea, North': 'KP', 
      'Italy': 'IT', 'Ecuador': 'EC', 'Somalia': 'SO', 'Syria': 'SY', 'Zambia': 'ZM', 
      'Burkina Faso': 'BF', 'Lebanon': 'LB', 'Romania': 'RO', 'Sri Lanka': 'LK', 'Azerbaijan': 'AZ', 
      'Madagascar': 'MG', 'Venezuela': 'VE', 'Austria': 'AT', 'Zimbabwe': 'ZW', 'Cambodia': 'KH', 
      'Sweden': 'SE', 'Cuba': 'CU', 'Belarus': 'BY', 'Netherlands': 'NL', 'Kazakhstan': 'KZ', 
      'Malawi': 'MW', 'Poland': 'PL', 'Puerto Rico': 'PR', 'Congo (Brazzaville)': 'CG', 'Oman': 'OM', 
      'Uruguay': 'UY', 'Honduras': 'HN', 'Uganda': 'UG', 'Guinea': 'GN', 'Bulgaria': 'BG', 
      'Costa Rica': 'CR', 'Rwanda': 'RW', 'Panama': 'PA', 'Senegal': 'SN', 'Mongolia': 'MN', 
      'Israel': 'IL', 'Denmark': 'DK', 'Finland': 'FI', 'Czechia': 'CZ', 'New Zealand': 'NZ', 
      'Dominican Republic': 'DO', 'Portugal': 'PT', 'Ireland': 'IE', 'Belgium': 'BE', 'Serbia': 'RS', 
      'Qatar': 'QA', 'Libya': 'LY', 'Burundi': 'BI', 'Mozambique': 'MZ', 'Kyrgyzstan': 'KG', 
      'Georgia': 'GE', 'Chad': 'TD', 'Mauritania': 'MR', 'Armenia': 'AM', 'Norway': 'NO', 
      'Nicaragua': 'NI', 'Turkmenistan': 'TM', 'Niger': 'NE', 'Liberia': 'LR', 'Haiti': 'HT', 
      'Eritrea': 'ER', 'Sierra Leone': 'SL', 'Laos': 'LA', 'Latvia': 'LV', 
      'Central African Republic': 'CF', 'Tajikistan': 'TJ', 'Nepal': 'NP', 'Gabon': 'GA', 
      'Croatia': 'HR', 'Lithuania': 'LT', 'Moldova': 'MD', 'Papua New Guinea': 'PG', 'Benin': 'BJ', 
      'Bahrain': 'BH', 'Estonia': 'EE', 'Djibouti': 'DJ', 'Tunisia': 'TN', 'Gaza Strip': 'PS', 
      'Jamaica': 'JM', 'Macau': 'MO', 'North Macedonia': 'MK', 'Guinea-Bissau': 'GW', 'Malta': 'MT', 
      'Paraguay': 'PY', 'Slovakia': 'SK', 'South Sudan': 'SS', 'Switzerland': 'CH', 'Namibia': 'NA', 
      'Bosnia and Herzegovina': 'BA', 'Albania': 'AL', 'Gambia, The': 'GM', 'Lesotho': 'LS', 
      'Cyprus': 'CY', 'El Salvador': 'SV', 'Reunion': 'RE', 'Equatorial Guinea': 'GQ', 'Slovenia': 'SI', 
      'Bahamas, The': 'BS', 'Martinique': 'MQ', 'Guadeloupe': 'GP', 'Botswana': 'BW', 'Suriname': 'SR', 
      'Timor-Leste': 'TL', 'Kosovo': 'XK', 'West Bank': 'PS', 'Guyana': 'GY', 'Fiji': 'FJ', 
      'New Caledonia': 'NC', 'Montenegro': 'ME', 'Curaçao': 'CW', 'Mauritius': 'MU', 'Iceland': 'IS', 
      'Maldives': 'MV', 'Luxembourg': 'LU', 'French Polynesia': 'PF', 'Guam': 'GU', 'Bhutan': 'BT', 
      'Togo': 'TG', 'Eswatini': 'SZ', 'Barbados': 'BB', 'Trinidad and Tobago': 'TT', 'Solomon Islands': 'SB', 
      'Mayotte': 'YT', 'Cabo Verde': 'CV', 'Saint Lucia': 'LC', 'Sao Tome and Principe': 'ST', 
      'French Guiana': 'GF', 'Belize': 'BZ', 'Brunei': 'BN', 'Vanuatu': 'VU', 'Samoa': 'WS', 
      'Monaco': 'MC', 'Aruba': 'AW', 'Gibraltar': 'GI', 'Jersey': 'JE', 'Marshall Islands': 'MH', 
      'Comoros': 'KM', 'Kiribati': 'KI', 'Isle of Man': 'IM', 'Cayman Islands': 'KY', 'Seychelles': 'SC', 
      'Saint Vincent and the Grenadines': 'VC', 'Tonga': 'TO', 'Andorra': 'AD', 
      'Antigua and Barbuda': 'AG', 'Guernsey': 'GG', 'Greenland': 'GL', 'Dominica': 'DM', 
      'Micronesia, Federated States of': 'FM', 'Faroe Islands': 'FO', 'Saint Kitts and Nevis': 'KN', 
      'Virgin Islands, British': 'VG', 'American Samoa': 'AS', 'Grenada': 'GD', 'San Marino': 'SM', 
      'Bonaire, Sint Eustatius, and Saba': 'BQ', 'Palau': 'PW', 'Tuvalu': 'TV', 'Liechtenstein': 'LI', 
      'Saint Martin': 'MF', 'Saint Pierre and Miquelon': 'PM', 'Cook Islands': 'CK', 
      'Turks and Caicos Islands': 'TC', 'Anguilla': 'AI', 'Northern Mariana Islands': 'MP', 
      'Saint Barthelemy': 'BL', 'Falkland Islands (Islas Malvinas)': 'FK', 'Sint Maarten': 'SX', 
      'Svalbard': 'SJ', 'Christmas Island': 'CX', 'Wallis and Futuna': 'WF', 'Bermuda': 'BM', 
      'Vatican City': 'VA', 'Nauru': 'NR', 'Saint Helena, Ascension, and Tristan da Cunha': 'SH', 
      'Niue': 'NU', 'Montserrat': 'MS', 'Norfolk Island': 'NF', 
      'South Georgia and South Sandwich Islands': 'GS', 'Pitcairn Islands': 'PN', 
      'South Georgia And South Sandwich Islands': 'GS', 'U.S. Virgin Islands': 'VI', 
      'DR Congo': 'CD', 'Myanmar': 'MM', 'South Korea': 'KR', "Côte d'Ivoire": 'CI', 
      'North Korea': 'KP', 'Czech Republic (Czechia)': 'CZ', 'Congo': 'CG', 
      'State of Palestine': 'PS', 'Gambia': 'GM', 'Micronesia': 'FM', 'Bahamas': 'BS', 
      'Sao Tome & Principe': 'ST', 'St. Vincent & Grenadines': 'VC', 'Saint Kitts & Nevis': 'KN', 
      'Holy See': 'VA', 'United Republic of Tanzania': 'TZ', 'Syrian Arab Republic': 'SY', 
      'United States of America': 'US', 'Russian Federation': 'RU', 'Democratic Republic of the Congo': 'CD', 
      'British Virgin Islands': 'VG', 'Viet Nam': 'VN', 'Czech Republic': 'CZ', 
      'Republic of Moldova': 'MD', 'Plurinational State of Bolivia': 'BO', 
      'The former Yugoslav Republic of Macedonia': 'MK', 'Ivory Coast': 'CI'
  }
  df['country_iso_assigned'] = df['country'].map(country_iso_map)
  return df


def remove_unwanted_words_and_numbers(text):
    # List of unwanted words
    unwanted_words = {
        'avenue', 'rd', 'road', 'blvd', 'boulevard', 'st', 'street', 'building', 'buildings', 'po', 'box', 'pobox', 'unknown'
    }
    
    # Remove specific special characters including '/', '-', '.', ',', apostrophes, single and double quotes
    text = re.sub(r'[\/\-,\.\!@#\$%\^&\*\(\)_\+=\'\"]', '', text)
    
    # Remove unwanted words
    words = text.split()
    words = [word for word in words if word not in unwanted_words]
    
    # Remove numbers and single-character substrings
    words = [word for word in words if not word.isdigit() and len(word) > 1]
    
    return " ".join(words)



def add_spaces_greedy(text, word_dict):
    i = 0
    result = []
    text = text.lower()

    while i < len(text):
        # Initialize variables for the longest word found
        longest_word = None
        longest_len = 0
        
        # Try to find the longest word in the dictionary that matches the current substring
        for j in range(i + 1, len(text) + 1):
            word = text[i:j]
            if word in word_dict and len(word) > longest_len:
                longest_word = word
                longest_len = len(word)
        
        # If a word was found, add it to the result
        if longest_word:
            result.append(longest_word)
            i += longest_len
        else:
            # If no word is found, move one character forward and add it as-is
            result.append(text[i])
            i += 1

    # Rejoin numeric sequences
    processed_text = " ".join(result)
    processed_text = re.sub(r'(\d)\s+(?=\d)', r'\1', processed_text)
    
    return processed_text