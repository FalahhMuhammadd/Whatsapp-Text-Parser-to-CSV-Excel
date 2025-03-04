import pandas as pd
from striprtf.striprtf import rtf_to_text
import re
import unicodedata

# Function for cleaning surrogate characters
def clean_surrogates(text):
    return ''.join(char for char in text if not (0xD800 <= ord(char) <= 0xDFFF))

# Function for reading RTF File
def read_rtf(file_path):
    with open(file_path, "rb") as file:
        rtf_content = file.read()

    # Convert RTF File to text using striprtf
    try:
        rtf_text = rtf_to_text(rtf_content.decode("utf-8", errors="ignore"))
    except UnicodeDecodeError:
        # If utf-8 failed, try using another encodings
        try:
            rtf_text = rtf_to_text(rtf_content.decode("latin-1", errors="ignore"))
        except Exception as e:
            st.error(f"Failed to read RTF: {e}")

    # Clean surrogate characters
    cleaned_text = clean_surrogates(rtf_text)

    # Normalize Unicode
    cleaned_text = unicodedata.normalize("NFKC", cleaned_text)

    return cleaned_text

# Function for parsing Whatsapp Chat
def parse_whatsapp_chat(text):
    pattern = re.compile(r'\[(\d{4}/\d{2}/\d{2}), (\d{1,2}:\d{2}:\d{2})\] ~\s*(.*?): (.*)')
    data = []

    for line in text.split("\n"):
        line = line.strip()
        match = pattern.match(line)
        if match:
            date, time, user, message = match.groups()
            data.append([date, time, user, message])

    df = pd.DataFrame(data, columns=["Date", "Time", "Username", "Message"])
    return df