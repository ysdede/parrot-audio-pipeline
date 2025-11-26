import openai
import pandas as pd


#update the file path
file_path="PARROT_v1_0.jsonl"

#loading the dataset
df = pd.read_json(file_path, lines=True)

reports = df['report']

#enter your API key here
openai_key=""

client = openai.OpenAI(api_key=openai_key)

#adapt the query to your use case
query = "Create a short patient summary in English for this radiology report. Use simple language that can be easily understood by patients. Here is the report: \n"

model="gpt-4o"

for report in reports:
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query+report}
                ],
            }
        ],
        temperature=0,
    )
    
    print(response.choices[0].message.content)