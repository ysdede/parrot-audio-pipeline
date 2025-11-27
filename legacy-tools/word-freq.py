import csv
from collections import defaultdict

def read_csv(file_path, delimiter='\t'):
    data = defaultdict(int)
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        for row in reader:
            sentence = row['Sentence']
            try:
                frequency = int(row['Frequency'])
            except Exception as e:
                print(row, e)
            for word in sentence.split():
                data[word] += frequency
    return data

def write_csv(sorted_data, output_file_path, delimiter='\t'):
    with open(output_file_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(['Sentence', 'Frequency'])
        
        for word, freq in sorted_data:
            writer.writerow([word, freq])

def main():
    input_file_path = 'sentences-raw.txt'
    output_file_path = 'word_frequencies-from-raw.csv'

    word_frequencies = read_csv(input_file_path)
    # Sort by total frequency
    sorted_word_frequencies = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
    write_csv(sorted_word_frequencies, output_file_path)

    print(f"Word frequencies written to {output_file_path}")

if __name__ == '__main__':
    main()
