from collections import defaultdict
import re
import ollama

def df_to_dictionary(df, col_name, char_limit):
    word_dict = defaultdict(int)

    # Regular expression pattern to match Chinese characters
    cn_regex = re.compile(r'[\u4e00-\u9fff]+')
    email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    llm_calls_count = 0
    
    # Iterate through each column in the DataFrame
    for address in df[col_name]:
        # Split on spaces, dashes, backslashes, forward slashes
        words = re.split(r'[ \-/\\]', address)
        
        # Check if any word is longer than char_limit characters (exclude chinese characters and emails)
        if len(address) < 300 and any(len(word) > char_limit and not cn_regex.search(word) and not email_regex.match(word) for word in words):
            llm_addr = llama_split_address(address)
            words = llm_addr.split()
            llm_calls_count += 1
        
        # Add words to the dictionary and count occurrences
        for word in words:
            word_dict[word] += 1

    print(f'Used the LLM {llm_calls_count} times')
    return word_dict


def llama_split_address(address):
    print(f'{address}')
    prompt = f'Given the following address, add spaces where necessary, do not add newlines, return only the address with appropriate spaces, do not respond with any other text: {address}'

    response = ollama.chat(
        model="llama3.1",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    content = response["message"]["content"]
    stripped_string = content.strip().strip('\n').strip('"').strip("'").replace('\n', ' ')
    print(f'{stripped_string}')
    print()
    return stripped_string
