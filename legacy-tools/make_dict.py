import csv
import re
import time

def get_line_count(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)

def find_unique_words(file_path):
    total_lines = get_line_count(file_path)
    unique_words = set()
    pattern = re.compile(r'\b\w+\b')
    processed_lines = 0
    start_time = time.time()

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            processed_lines += 1
            if row:  # Ensure the row is not empty
                sentence = row[0]  # First column contains the sentence
                words = pattern.findall(sentence)
                unique_words.update(words)

            # Progress and remaining time calculation
            if processed_lines % 100 == 0:  # Update every 100 lines
                elapsed_time = time.time() - start_time
                progress = (processed_lines / total_lines) * 100
                estimated_total_time = (elapsed_time / processed_lines) * total_lines
                remaining_time = estimated_total_time - elapsed_time
                print(f"Processed: {processed_lines}/{total_lines} lines ({progress:.2f}%), Remaining time: {remaining_time:.2f} seconds")

    return unique_words

# File path
file_path = 'aggregated_sentences-raw-2nd.csv'

# Find unique words
unique_words = find_unique_words(file_path)

import json

def save_words_to_json(unique_words, output_file):
    # Convert words to a dictionary assigning a unique ID to each word
    words_dict = {word: idx for idx, word in enumerate(unique_words)}

    # Save as JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(words_dict, f, ensure_ascii=False, indent=4)

# Save unique words to a JSON file
output_file = 'unique_words.json'
save_words_to_json(unique_words, output_file)
