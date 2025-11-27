import os
import re
import time
from collections import Counter
from striprtf.striprtf import rtf_to_text
from utils import translate, delete_sentence_if_found

# Create a set of sentences to drop based on blacklist
drop_sentence_if_found = set(delete_sentence_if_found)

# Compile the year pattern once (matches 8‑11 digit numbers where the first four digits are a year between 1990 and 2023)
year_pattern = re.compile(r"\b(19[9][0-9]|20[0-2][0-9]|2023)\d{4,7}\b")

def clean_and_split_sentence(sentence):
    """Apply translation replacements and strip trailing punctuation from a sentence."""
    for key, value in translate.items():
        sentence = sentence.replace(key, value)
    return re.sub(r'[.:",;]+$', '', sentence.strip())

def is_sentence_valid(sentence, current_progress, elapsed_time):
    """Return False if the sentence contains a black‑listed word or matches the year pattern, printing progress info."""
    if any(word in sentence for word in delete_sentence_if_found):
        remaining_time = (elapsed_time / current_progress) * (100 - current_progress)
        print(f"Skipped (Keyword) at {current_progress:.2f}%: {sentence} - Elapsed: {elapsed_time:.2f}s, Remaining: {remaining_time:.2f}s")
        return False
    if year_pattern.search(sentence):
        remaining_time = (elapsed_time / current_progress) * (100 - current_progress)
        print(f"Skipped (Pattern) at {current_progress:.2f}%: {sentence} - Elapsed: {elapsed_time:.2f}s, Remaining: {remaining_time:.2f}s")
        return False
    return True

def process_text(text, current_progress, elapsed_time):
    """Split the text into sentences, clean them, and keep only valid ones."""
    sentences = re.split(r'(?<=\.)\s+|\.{2,}|\n', text.lower())
    return [clean_and_split_sentence(sentence) for sentence in sentences if is_sentence_valid(sentence, current_progress, elapsed_time)]

def convert_rtf_to_text(rtf_path):
    """Read an RTF file and convert it to plain text."""
    try:
        with open(rtf_path, 'r', encoding='utf-8') as file:
            return rtf_to_text(file.read()).replace("\n\n", "\n")
    except Exception as e:
        print(f"Error converting {rtf_path}: {e}")
        return None

def main():
    # List of RTF files to process
    rtf_list_file = "dictation_rtfs.txt"
    with open(rtf_list_file, 'r', encoding='utf-8') as file:
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
            frequency.update(process_text(text, progress, elapsed_time))

    # Write the aggregated sentence frequencies to a TSV file
    output_file = "sentences-new.csv"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("Sentence\tFrequency\n")
        for sentence, freq in frequency.most_common():
            file.write(f"{sentence}\t{freq}\n")

if __name__ == "__main__":
    main()
