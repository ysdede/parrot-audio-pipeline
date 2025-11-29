import re
from collections import Counter

file_path = "PARROT_v1_0_052_transcription_fixed.txt"

with open(file_path, 'r', encoding='utf-8') as f:
    translations = [line.strip() for line in f.readlines() if line.strip()]

all_phrases = []
for translation in translations:
    # Normalize literal newlines
    translation = translation.replace('\\n', ' ')
    # Split into words
    words = re.findall(r'\b\w+\b', translation)
    
    # Get 3-6 word phrases
    for n in range(3, 7):
        if len(words) >= n:
            for i in range(len(words) - n + 1):
                phrase = ' '.join(words[i:i+n])
                all_phrases.append(phrase)

# Count and filter
phrase_counter = Counter(all_phrases)
frequent_phrases = [(phrase, count) for phrase, count in phrase_counter.items() if count >= 20]
frequent_phrases.sort(key=lambda x: x[1], reverse=True)

print(f"Total frequent phrases: {len(frequent_phrases)}")
for phrase, count in frequent_phrases[:50]:
    print(f"{count}: {phrase}")

# Check specifically for WiRXh
print("\nChecking for WiRXh phrases:")
wirxh_phrases = [p for p in frequent_phrases if 'WiRXh' in p[0]]
for phrase, count in wirxh_phrases:
    print(f"{count}: {phrase}")
