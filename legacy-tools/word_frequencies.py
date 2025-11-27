import csv
import re
import time
from collections import defaultdict
import json

def get_line_count(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)

def find_unique_words_and_frequencies(file_path):
    total_lines = get_line_count(file_path)
    word_frequencies = defaultdict(int)  # Count word frequencies
    pattern = re.compile(r'\b\w+\b')
    processed_lines = 0
    start_time = time.time()

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        # Skip the first row (header)
        next(reader)
        for row in reader:
            processed_lines += 1
            if row:
                sentence = row[0]  # The first column contains the sentence
                words = pattern.findall(sentence)
                for word in words:
                    word_frequencies[word] += 1 * int(row[1])  # Increase word frequency by the sentence weight

            # Progress and remaining time calculation
            if processed_lines % 100 == 0:
                elapsed_time = time.time() - start_time
                progress = (processed_lines / total_lines) * 100
                estimated_total_time = (elapsed_time / processed_lines) * total_lines
                remaining_time = estimated_total_time - elapsed_time
                print(f"Processed: {processed_lines}/{total_lines} rows ({progress:.2f}%), Remaining time: {remaining_time:.2f} seconds")

    return word_frequencies

def save_sorted_frequencies_to_json(word_frequencies, output_file):
    # Sort by frequency (highest to lowest)
    sorted_frequencies = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)

    # Save in JSON format
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sorted_frequencies, f, ensure_ascii=False)

file_path = 'aggregated_sentences-raw-2nd.csv'
output_file = 'sorted_word_frequencies.json'
# Find unique words and their frequencies
word_frequencies = find_unique_words_and_frequencies(file_path)

save_sorted_frequencies_to_json(word_frequencies, output_file)
