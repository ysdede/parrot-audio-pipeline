from elasticsearch import Elasticsearch, helpers
import os

CERT_FINGERPRINT = "efededededede"
ELASTIC_PASSWORD = "efededededede"
# Connect to Elasticsearch server
es = Elasticsearch(
    "https://localhost:9200",
    ssl_assert_fingerprint=CERT_FINGERPRINT,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

# Successful response!
es.info()

# Define index name
index_name = "dictation_texts"

def create_document(file_path, author_id):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        # Use parent folder name as ID
        document_id = os.path.basename(os.path.dirname(file_path))
        return {
            "_index": index_name,
            "_source": {
                "id": document_id,
                "content": content,
                "author_id": author_id  # Add author ID
            }
        }
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def index_documents(file_list, author_id):
    # Read file list and add each file to Elasticsearch
    actions = []
    with open(file_list, 'r') as file:
        for line in file:
            file_path = line.strip()
            doc = create_document(file_path, author_id)
            if doc:
                actions.append(doc)
    
    # Add document collection to Elasticsearch in bulk
    if actions:
        helpers.bulk(es, actions)

# File list and author ID
file_list = "DictationTxt.txt"
author_id = 45  # Example author ID

# Document indexing process
index_documents(file_list, author_id)
print("Indexing completed.")
