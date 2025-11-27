import csv
from collections import Counter

def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        sentences = [row['Sentence'] for row in reader]
    return sentences

def find_duplicates(sentences):
    counter = Counter(sentences)
    return [sentence for sentence, count in counter.items() if count > 1]

def main():
    file_path = 'sentences-new.csv'  # File path
    sentences = read_csv(file_path)
    duplicates = find_duplicates(sentences)

    for sentence in duplicates:
        print(f'Duplicate: "{sentence}"')

if __name__ == '__main__':
    main()
