import csv
import re
import time
import pandas as pd
import collections

pattern = re.compile(r"\b\w+\b")

# Paths to input files
corpus_path = "aggregated_sentences-raw-2nd.csv"
error_words_path = "error_words.txt"

# Load error words list
error_words = []
with open(error_words_path, "r", encoding="utf-8") as file:
    error_words = file.read().splitlines()

# Load corpus as raw text
with open(corpus_path, "r", encoding="utf-8") as file:
    corpus = file.read()


def check_word_in_column(string_to_lookup, column_name="Sentence"):
    # Check if the string is in the DataFrame column (placeholder implementation)
    count = corpus[column_name].str.contains(string_to_lookup).sum()
    print(f"{string_to_lookup} {count}")
    return count

errors_list_in_corpus = []

total_lines_to_check = len(error_words)
start_time = time.time()
for index, word in enumerate(error_words):
    ec = corpus.count(word)

    if ec > 0:
        errors_list_in_corpus.append(ec)

    elapsed_time = time.time() - start_time
    avg_iter_time = elapsed_time / (index + 1)
    remaining_iter = total_lines_to_check - index
    calculated_eta = remaining_iter * avg_iter_time / 60
    print(f"{index:<8}{word:<32} {ec:<5} {calculated_eta:<8.1f} min")

# Exit after processing
exit()

number_of_words = 0
number_of_sentences = 0

decompressed_corpus = ""
i = 0
with open(corpus_path, "r", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter="\t")
    # Skip header row
    next(reader)
    for row in reader:
        if row:
            # Duplicate the sentence row[0] according to its frequency row[1]
            decompressed_corpus += row[0] * int(row[1]) + "\n"
            number_of_sentences += int(row[1])
            number_of_words += len(pattern.findall(row[0])) * int(row[1])
            i += 1
        print(i, end=",")

print(f"Number of Sentences: {number_of_sentences}, Number of Words: {number_of_words}")
print(f"Decompressed Corpus Size: {len(decompressed_corpus)}")
print(f"Decompressed Corpus Size (Bytes): {len(decompressed_corpus.encode())}")

with open("decompressed_corpus.txt", "w", encoding="utf-8") as file:
    file.write(decompressed_corpus)
