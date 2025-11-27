from collections import Counter

report_file = "C:/text-files/example.txt"
report_file += "/text.txt"

with open(report_file, "r", encoding="utf-8") as file:
    text = file.read()

text = text.replace("[", "").replace("]", "").replace("{", "").replace("}", "").replace("Findings\n", "").replace("Findings:\n", "")

# Function to split sentences
def split_sentences(text):
    sentences = []
    sentence_start = 0
    for i in range(len(text)):
        if text[i] == ":" or text[i] == "\n" or (text[i] == "." and (i + 1 == len(text) or text[i + 1] in [" ", "\n"])):
            sentence = text[sentence_start:i+1].strip()
            if sentence:
                sentences.append(sentence)
            sentence_start = i + 1
    return sentences

# Split sentences
separated_sentences = split_sentences(text)

# Calculate frequency
frequency = Counter(separated_sentences)

# Print unique sentences and their frequencies
for sentence, freq in frequency.items():
    print(f"Sentence: '{sentence}' - Frequency: {freq}")
