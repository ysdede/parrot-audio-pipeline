#pip install ollama
from ollama import chat
from ollama import ChatResponse
import pandas as pd


#update the file path
file_path="PARROT_v1_0.jsonl"

#loading the dataset
df = pd.read_json(file_path, lines=True)

reports = df['report']

#adapt this query based on your use case
query = "Create a short patient summary in English for this radiology report. Use simple language that can be easily understood by patients. Here is the report: \n"

for report in reports:

    response: ChatResponse = chat(model='llama3.3', messages=[
      {
        'role': 'user',
        'content': query+report,
      },
    ])
    print(response['message']['content'])
