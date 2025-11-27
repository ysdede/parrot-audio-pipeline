import csv
import re
import time

pattern = re.compile(r"\b\w+\b")

corpus_path = "aggregated_sentences-raw-2nd.csv"
error_words_path = "error_words.txt"

error_words = []

with open(error_words_path, "r", encoding="utf-8") as file:
    error_words = file.read().splitlines()

with open(corpus_path, "r", encoding="utf-8") as file:
    corpus = file.read()


def check_word_in_column(string_to_lookup, column_name="Sentence"):
    count = 0
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
