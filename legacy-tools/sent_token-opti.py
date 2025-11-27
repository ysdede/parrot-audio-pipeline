import os
from striprtf.striprtf import rtf_to_text
from collections import Counter
from utils import translate, delete_sentence_if_found
import re

def convert_rtf_to_txt(rtf_path, current, total):
    """Convert an RTF file to plain text."""
    try:
        with open(rtf_path, 'r', encoding='utf-8') as file:
            rtf_content = file.read()
        text_content = rtf_to_text(rtf_content).replace("\n\n", "\n")
        progress = (current / total) * 100
        # Optional progress output
        # print(f"Converted {rtf_path} [{progress:.2f}%]")
        return text_content
    except Exception as e:
        print(f"Error converting {rtf_path}: {e}")
        return None

def split_and_clean_sentences(text):
    """Apply translation dictionary, split into sentences, and clean them."""
    # Apply translation replacements
    for key, value in translate.items():
        text = text.replace(key, value)

    # Split sentences (period followed by space, multiple periods, or newline)
    sentences = re.split(r'(?<=\.)\s+|\.{2,}|\n', text)

    cleaned_sentences = []

    # Pattern for 8-11 digit numbers where the first four digits represent a year between 1990 and 2023
    pattern = re.compile(r'\b(19[9][0-9]|20[0-2][0-9]|2023)\d{4,7}\b')

    for sentence in sentences:
        # Skip sentences containing blacklisted words
        if any(word in sentence for word in delete_sentence_if_found):
            continue
        sentence = sentence.strip()
        # Skip sentences matching the numeric pattern
        if pattern.search(sentence):
            continue
        if sentence:
            # Remove trailing punctuation . : , ; "
            sentence = re.sub(r'[.:",;]+$', '', sentence)
            cleaned_sentences.append(sentence)
    return cleaned_sentences

# Read list of RTF files
rtf_list_file = "dictation_rtfs.txt"
with open(rtf_list_file, 'r', encoding='utf-8') as file:
    rtf_paths = file.readlines()

total_files = len(rtf_paths)
frequency = Counter()
for index, path in enumerate(rtf_paths):
    rtf_path = path.strip()
    progress = ((index + 1) / total_files) * 100
    text = convert_rtf_to_txt(rtf_path, index + 1, total_files)
    if text is None:
        continue
    text = text.lower()
    sentences = split_and_clean_sentences(text)
    frequency.update(sentences)

sorted_frequencies = frequency.most_common()

# Write sorted results to file
output_file = "sentences-new.txt"
with open(output_file, "w", encoding="utf-8") as file:
    for sentence, freq in sorted_frequencies:
        file.write(f"{sentence} {freq}\n")
