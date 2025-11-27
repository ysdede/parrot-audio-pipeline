import json


def load_words_from_json(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        return json.load(f)

import os
import re
import time
from collections import Counter
from striprtf.striprtf import rtf_to_text
from utils import translate, delete_sentence_if_found

# Compile regex patterns once
year_pattern = re.compile(r'\b(19[9][0-9]|20[0-2][0-9]|2023)\d{4,7}\b')
word_pattern = re.compile(r'\b\w+\b')

def clean_and_split_sentence(sentence):
    for key, value in translate.items():
        sentence = sentence.replace(key, value)
    return re.sub(r'[.:",;]+$', '', sentence.strip())

def is_sentence_valid(sentence, current_progress, elapsed_time):
    if any(word in sentence for word in delete_sentence_if_found):
        remaining_time = (elapsed_time / current_progress) * (100 - current_progress)
        print(f"Skipped (Keyword) at {current_progress:.2f}%: {sentence} - Elapsed: {elapsed_time:.2f}s, Remaining: {remaining_time/60:.1f} mins.")
        return False
    if year_pattern.search(sentence):
        remaining_time = (elapsed_time / current_progress) * (100 - current_progress)
        print(f"Skipped (Pattern) at {current_progress:.2f}%: {sentence} - Elapsed: {elapsed_time:.2f}s, Remaining: {remaining_time/60:.1f} mins.")
        return False
    return True

def process_text(text, current_progress, elapsed_time):
    # sentences = re.split(r'(?<=\.)\s+|\.{2,}|\n', text.lower())
    sentences = re.split(r'(?<=\.)\s+|\.{2,}|\n', text)
    return [clean_and_split_sentence(sentence) for sentence in sentences if is_sentence_valid(sentence, current_progress, elapsed_time)]

def convert_rtf_to_text(rtf_path):
    try:
        with open(rtf_path, 'r') as file:
            return rtf_to_text(file.read()).replace("\n\n", "\n")
    except Exception as e:
        print(f"Error converting {rtf_path}: {e}")
        return None

def main():
    orphan_words = []
    # Load JSON file
    words_dict = load_words_from_json("unique_words.json")

    rtf_list_file = "DictationRtfs.txt"
    with open(rtf_list_file, "r") as file:
        rtf_paths = file.readlines()

    total_files = len(rtf_paths)
    frequency = Counter()

    start_time = time.time()

    for index, path in enumerate(rtf_paths):
        rtf_path = path.strip()
        progress = (index + 1) / total_files * 100
        elapsed_time = time.time() - start_time
        text = convert_rtf_to_text(rtf_path)

        if text:
            # print(text, type(text))
            s = process_text(text, progress, elapsed_time)
            # print(s, type(s))
            # exit()
            for line in s:
                if line:
                    words = word_pattern.findall(line)
                    for w in words:
                        if w not in words_dict:
                            orphan_words.append(w)
                            print(w, end=' -- ')
    
    # count number of occurrences of each word
    for word in orphan_words:
        frequency[word] += 1
    
    # sort by frequency
    frequency = frequency.most_common()
    print(frequency)

    # with open("sentences-new.csv", "w") as file:
    #     file.write("Sentence\tFrequency\n")
    #     for sentence, freq in frequency.most_common():
    #         file.write(f"{sentence}\t{freq}\n")


if __name__ == "__main__":
    main()
