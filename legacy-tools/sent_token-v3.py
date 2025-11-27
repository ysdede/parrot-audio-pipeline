import csv
import os
import re
import time
from collections import Counter
from striprtf.striprtf import rtf_to_text
from utils import translate, delete_sentence_if_found

drop_sentence_if_found = set(delete_sentence_if_found)

frequency = Counter()
unformatted_documents = []
examinations = []
summaries = []
diagnostics = []
processed_count = 0
error_count = 0

processed_rows = []
id_rtf = []

# Capture ctrl-c
import signal


def signal_handler(sig, frame):
    print("You pressed Ctrl+C!")
    save_results()
    exit(0)


def save_results():
    with open("UNFORMATTED_DOCUMENTS.txt", "w", encoding="utf-8") as file:
        for path, lines in unformatted_documents:
            file.write(f"{path}\n")
            for line in lines:
                file.write(f"{line}\n")
            file.write("\n")

    with open("EXAMINATIONS.txt", "w", encoding="utf-8") as file:
        for examination in examinations:
            file.write(f"{examination}\n")

    with open("SUMMARIES.txt", "w", encoding="utf-8") as file:
        for summary in summaries:
            file.write(f"{summary}\n")

    with open("DIAGNOSTICS.txt", "w", encoding="utf-8") as file:
        for diagnostic in diagnostics:
            file.write(f"{diagnostic}\n")

    with open("CORPUS.tsv", "w", encoding="utf-8") as file:
        for sentence, freq in frequency.items():
            file.write(f"{sentence}\t{freq}\n")

    with open("processed_rows.tsv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerows(processed_rows)
    
    with open("id_rtf.tsv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerows(id_rtf)


# Set handler for Ctrl-C signal
signal.signal(signal.SIGINT, signal_handler)

# Compile regex patterns once
year_pattern = re.compile(r"\b(19[9][0-9]|20[0-2][0-9]|2023)\d{4,7}\b")


def clean_and_strip(sentence):
    for key, value in translate.items():
        sentence = sentence.replace(key, value)
    return sentence.strip().replace("\n", " <NL> ")


def is_sentence_valid(sentence, current_progress, elapsed_time):
    for word in delete_sentence_if_found:
        if word in sentence:
            remaining_time = (elapsed_time / current_progress) * (
                100 - current_progress
            )
            print(
                f"Skipped (Keyword '\033[93m{word}\033[0m') at {current_progress:.2f}%: {sentence} - Elapsed: {elapsed_time:.2f}s, Remaining: {remaining_time:.2f}s"
            )
            return False
    if year_pattern.search(sentence):
        remaining_time = (elapsed_time / current_progress) * (100 - current_progress)
        print(
            f"Skipped (Pattern) at {current_progress:.2f}%: {sentence} - Elapsed: {elapsed_time:.2f}s, Remaining: {remaining_time:.2f}s"
        )
        return False
    return True


def process_text(text, current_progress, elapsed_time):
    # If text is valid, clean and strip it
    if is_sentence_valid(text, current_progress, elapsed_time):
        return clean_and_strip(text)

    # Split text into sentences and discard problematic ones
    sentences = re.split(r"(?<=\.)\s+|\.{2,}|\n", text)
    valid_sentences = [
        clean_and_strip(sentence)
        for sentence in sentences
        if is_sentence_valid(sentence, current_progress, elapsed_time)
    ]

    # Join valid sentences into a single string
    return " ".join(valid_sentences)


def convert_rtf_to_text(rtf_path):
    try:
        with open(rtf_path, "r", encoding="utf-8") as file:
            return rtf_to_text(file.read()).replace("\n\n", "\n")
    except Exception as e:
        print(f"Error converting {rtf_path}: {e}")
        return None


if __name__ == "__main__":
    rtf_list_file = "dictation_rtfs.txt"
    # rtf_list_file = "dictation_rtfs_short.txt"

    with open(rtf_list_file, "r", encoding="utf-8") as file:
        rtf_paths = file.readlines()

    total_files = len(rtf_paths)

    start_time = time.time()

    for index, path in enumerate(rtf_paths):
        rtf_path = path.strip()
        progress = (index + 1) / total_files * 100
        elapsed_time = time.time() - start_time
        text = convert_rtf_to_text(rtf_path)
        if len(text) < 20:
            continue

        if text:
            import re

            # Find text within [] and {}
            summary_pattern = r"\[([^]]+)\]"
            diagnostic_pattern = r"\{([^}]+)\}"

            # Assign found text to variables
            summary = re.search(summary_pattern, text)
            diagnostic = re.search(diagnostic_pattern, text)

            if summary:
                summary = summary.group(1)
                text = re.sub(summary_pattern, "", text)
                summary = clean_and_strip(summary)
                summaries.append(summary)
            else:
                summary = "<NONE>"
                summaries.append(summary)

            if diagnostic:
                diagnostic = diagnostic.group(1)
                text = re.sub(diagnostic_pattern, "", text)
                diagnostic = clean_and_strip(diagnostic)
                diagnostics.append(diagnostic)
            else:
                diagnostic = "<NONE>"
                diagnostics.append(diagnostic)

            import re

            # Get first four lines
            first_four_lines = [line.strip() for line in text.split("\n")[:4]]

            # Find lines ending with ':'
            colon_end_pattern = r".*:$"
            colon_end_matches = [
                line for line in first_four_lines if re.search(colon_end_pattern, line)
            ]

            # Find lines starting with 'examination:' (tetkik)
            examination_start_pattern = r"(?i)^(tetkik|examination):.*"
            examination_start_matches = [
                line
                for line in first_four_lines
                if re.search(examination_start_pattern, line)
            ]

            # Find lines ending with 'examination.' or 'examination' (tetkiki)
            examination_end_pattern = r"(?i)(tetkiki|examination)\.?$"
            examination_end_matches = [
                line
                for line in first_four_lines
                if re.search(examination_end_pattern, line)
            ]

            # Pattern for additional control keywords (medical imaging terms)
            # Turkish -> English: İNCELEMESİ=EXAMINATION, GRAFİSİ/GRAFİ=RADIOGRAPH, 
            # TETKİK=EXAMINATION, MEME=BREAST, USG/US=ULTRASOUND, MR/MRG=MRI, 
            # BT=CT, EKLEM=JOINT, KONTROL=CONTROL/FOLLOW-UP, KONSÜLTASYON=CONSULTATION,
            # MASTEKTOM=MASTECTOMY, İŞARETLEME=MARKING
            extra_keywords_pattern = r"(?i)(İNCELEMESİ|EXAMINATION|GRAFİSİ|GRAFİSİNDE|GRAFİLERİ|RADIOGRAPH|TETKİK|TETKİKİ|GRAFİ|3 BOYUTLU BT|3D CT|Kontrol|CONTROL|FOLLOW-UP|MEME US|BREAST US|tedavi planlamas|TREATMENT PLANNING|MRG|MRI| MR|USG|ULTRASOUND|MASTEKTOM|MASTECTOMY| US|MEME|BREAST|EKLEM|JOINT|İŞARETLEME|MARKING|KONTROL|KONSÜLTASYON|CONSULTATION|mastektomi| BT| CT|öyküsü|HISTORY)"

            extra_keywords_matches = [
                line
                for line in first_four_lines
                if re.search(extra_keywords_pattern, line)
            ]

            # Control order
            matches = (
                colon_end_matches
                if colon_end_matches
                else (
                    examination_start_matches
                    if examination_start_matches
                    else (
                        examination_end_matches
                        if examination_end_matches
                        else extra_keywords_matches
                    )
                )
            )

            if len(matches) > 0:
                text = text.replace(matches[0], "", 1)
                examination = clean_and_strip(matches[0])
                examinations.append(matches[0])
                
            else:
                examination = "<NONE>"
                examinations.append(examination)
                error_count += 1
                unformatted_documents.append((rtf_path, first_four_lines))

            processed_count += 1
            print(
                f"{error_count}/{processed_count} - {progress:.2f}% - {elapsed_time:.2f}s - {rtf_path}"
            )
            text = process_text(text, progress, elapsed_time)
            # Create a TSV and add processed_count as index, examination, text, summary, diagnostic
            processed_rows.append(
                (
                    processed_count,
                    examination,
                    text,
                    summary,
                    diagnostic
                )
            )

            id_rtf.append(
                (
                    processed_count,
                    rtf_path.replace("file-path", "").replace("\\", "/"),
                )
            )

            frequency.update(text.split())

    save_results()
