from collections import Counter
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
# Use English stopwords
stop_words = set(stopwords.words('english'))

import Levenshtein

def similarity(word1, word2):
    """Return Levenshtein similarity ratio between two strings."""
    return Levenshtein.ratio(word1, word2)


def fetch_all_documents(es_client, index):
    """Retrieve all documents from an Elasticsearch index."""
    query = {"query": {"match_all": {}}}
    documents = helpers.scan(
        es_client,
        query=query,
        index=index,
        scroll='5m',
        size=1000
    )
    return [doc['_source'] for doc in documents]


def process_text(text):
    """Tokenize text into words and sentences, removing stopwords."""
    words = word_tokenize(text.lower())
    sentences = sent_tokenize(text)
    filtered_words = [word for word in words if word not in stop_words and word.isalpha()]
    return filtered_words, sentences


def load_from_file(file_path):
    """Load lines from a file into a list."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]


def define_word_thresholds(words, common_threshold=10, rare_threshold=3):
    """Separate words into common and rare based on frequency thresholds."""
    word_counter = Counter(words)
    print("Sample word frequencies:", word_counter.most_common(10))
    common_words = [word for word, count in word_counter.items() if count >= common_threshold]
    rare_words = [word for word, count in word_counter.items() if count <= rare_threshold]
    return common_words, rare_words

# Load unique words and common sentences from files
unique_words = load_from_file('unique_words.txt')
common_sentences = load_from_file('common_sentences.txt')

print(f'Loaded {len(unique_words)} unique words and {len(common_sentences)} common sentences')

common_words, rare_words = define_word_thresholds(unique_words)

print(f"Number of common words: {len(common_words)}")
print(f"Number of rare words: {len(rare_words)}")

# Detect potential typos
potential_typos = []
for rare_word in rare_words:
    for common_word in common_words:
        if similarity(rare_word, common_word) > 0.8:
            print(f"Typo found: {rare_word} - {common_word}")
            potential_typos.append((rare_word, common_word))

formatted_typos = [f"{typo[0]} - {typo[1]}" for typo in potential_typos]

# Write the formatted strings to a file
with open('output_typos.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(formatted_typos))

print("Typo detection completed.")
