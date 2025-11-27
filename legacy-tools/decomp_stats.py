import csv
import re

pattern = re.compile(r'\b\w+\b')

file_path = "aggregated_sentences-raw-2nd.csv"
number_of_words = 0
number_of_sentences = 0
unique_words = set()
unique_sentences = set()

with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader)  # Skip the first line
    for row in reader:
        if row:
            sentence = row[0]  # The first column contains the sentence
            words = pattern.findall(sentence)
            unique_sentences.add(sentence)
            unique_words.update(words)
            number_of_sentences += int(row[1])
            number_of_words += len(words)

print(f"Number of Sentences: {number_of_sentences}")
print(f"Number of Words: {number_of_words}")
print(f"Number of Unique Sentences: {len(unique_sentences)}")
print(f"Number of Unique Words: {len(unique_words)}")
