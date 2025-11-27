import csv
from collections import defaultdict

def read_and_aggregate_frequencies(file_path):
    # Dictionary to store sentences and their total frequencies
    aggregated_data = defaultdict(int)

    # Read the file and aggregate frequencies
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        # count row number while iterating over reader
        # for row in reader:
        for index, row in enumerate(reader):
            sentence = row['Sentence']  # .strip()
            try:
                frequency = int(row['Frequency'])
            except Exception as e:
                print(e, sentence, " ", row, " ", frequency, type(frequency), index)
                # if not frequency:
                #     frequency = 1
                # else:
                #     frequency = int(frequency)

                frequency = 1
                if sentence.endswith(" 1"):
                    sentence = sentence[:-2]
            
                print('After fixing frequency:', frequency)
                print(sentence, "--", frequency, "--", type(frequency), "--", index)

            aggregated_data[sentence] += frequency

    return aggregated_data

def write_aggregated_data_to_csv(aggregated_data, output_file_path):
    # Write aggregated data to a new CSV file
    with open(output_file_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(['Sentence', 'Frequency'])
        for sentence, total_freq in aggregated_data.items():
            writer.writerow([sentence, total_freq])

def main():
    input_file_path = 'aggregated_sentences-raw.csv'   # Input file path
    output_file_path = 'aggregated_sentences-raw-2nd.csv'  # Output file path

    aggregated_data = read_and_aggregate_frequencies(input_file_path)
    write_aggregated_data_to_csv(aggregated_data, output_file_path)

    print(f"Aggregated data written to {output_file_path}")

if __name__ == '__main__':
    main()
