"""
Extract the 'translation' column from the CSV file and save it to a plain text file.

This script:
1. Reads the CSV file from the previous transformation step
2. Extracts the 'translation' column content
3. Saves each translation as a separate line in a text file
"""

import csv
import os

# Define input and output paths
INPUT_CSV = "../01_convert_jsonl_to_csv/PARROT_v1_0_escaped.csv"
OUTPUT_TXT = "PARROT_v1_0_translations.txt"

def extract_translation_column(input_csv_path, output_txt_path):
    """
    Extract the 'translation' column from CSV and write to a text file.
    
    Args:
        input_csv_path: Path to the input CSV file
        output_txt_path: Path to the output text file
    """
    translations = []
    translation_count = 0
    
    print(f"Reading from: {input_csv_path}")
    
    # Read the CSV file and extract the translation column
    with open(input_csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            if 'translation' in row:
                translation = row['translation']
                translations.append(translation)
                translation_count += 1
                
                # Print progress every 100 rows
                if translation_count % 100 == 0:
                    print(f"Processed {translation_count} translations...")
    
    # Write translations to text file
    print(f"\nWriting {len(translations)} translations to: {output_txt_path}")
    
    with open(output_txt_path, 'w', encoding='utf-8') as txtfile:
        for translation in translations:
            # Write each translation on a new line
            txtfile.write(translation + '\n')
    
    print(f"\nSuccessfully extracted {translation_count} translations!")
    print(f"Output file: {output_txt_path}")
    
    # Print statistics
    total_chars = sum(len(t) for t in translations)
    avg_length = total_chars / len(translations) if translations else 0
    
    print(f"\nStatistics:")
    print(f"  Total translations: {translation_count}")
    print(f"  Total characters: {total_chars:,}")
    print(f"  Average length: {avg_length:.1f} characters")

if __name__ == "__main__":
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Resolve paths relative to script location
    input_path = os.path.join(script_dir, INPUT_CSV)
    output_path = os.path.join(script_dir, OUTPUT_TXT)
    
    # Verify input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        exit(1)
    
    # Extract translations
    extract_translation_column(input_path, output_path)
