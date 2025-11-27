from collections import Counter
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
# Use English stopwords
stop_words = set(stopwords.words('english'))

from elasticsearch import Elasticsearch, helpers

# Connection details
CERT_FINGERPRINT = "efededededede"
ELASTIC_PASSWORD = "efededededede"

# Connect to Elasticsearch server
es = Elasticsearch(
    "https://localhost:9200",
    ssl_assert_fingerprint=CERT_FINGERPRINT,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

# Define index name
index_name = "dictation_texts"

def fetch_all_documents(es_client, index):
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
    # Tokenize words and sentences
    words = word_tokenize(text.lower())
    sentences = sent_tokenize(text)
    
    # Filter out stop words
    filtered_words = [word for word in words if word not in stop_words and word.isalpha()]
    
    return filtered_words, sentences

# Assuming `fetch_all_documents` is a function that retrieves all document contents
all_documents = fetch_all_documents(es, index_name)

# Initialize counters
word_counter = Counter()
sentence_counter = Counter()

for doc in all_documents:
    words, sentences = process_text(doc['content'])
    word_counter.update(words)
    sentence_counter.update(sentences)

# Get unique words and common sentences
unique_words = list(word_counter)
common_sentences = [sentence for sentence, count in sentence_counter.items() if count > 1]  # Adjust threshold as needed

# For medical terms, you would filter `unique_words` based on a medical dictionary
# Save unique words to file, save common sentences to file

with open('unique_words.txt', 'w') as file:
    file.write('\n'.join(unique_words))

with open('common_sentences.txt', 'w') as file:
    file.write('\n'.join(common_sentences))

