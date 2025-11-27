import pandas as pd

# Enter your file path here
file_path = 'sentences-raw.csv'

# Load the TAB-separated CSV file
df = pd.read_csv(file_path, sep='\t')

# Check and fix the frequency column
def fix_frequency(freq):
    try:
        return int(freq)
    except ValueError:
        print('Frequency error:', freq)
        return 1  # Default value

df['Frequency'] = df['Frequency'].apply(fix_frequency)

# Fix accidentally added TAB characters
def fix_sentence(sentence):
    try:
        r = ' '.join(sentence.split('\t'))
    except Exception as e:
        print(e, sentence)
        exit(1)
    return r

df['Sentence'] = df['Sentence'].apply(fix_sentence)

# Check and remove invalid rows
df = df[df['Sentence'].str.strip().astype(bool)]

# Save the corrected file
df.to_csv('sentences-raw-fixed.csv', sep='\t', index=False)
