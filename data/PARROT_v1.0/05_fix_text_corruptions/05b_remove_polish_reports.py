"""
Remove reports containing Polish characters from the corpus.

This script:
1. Reads the cleaned corpus line by line
2. Identifies reports containing Polish-specific characters
3. Saves Polish reports to a separate file
4. Saves English-only reports to the main corpus
5. Reports statistics on the separation
"""

import os
import re

# Define input and output paths
INPUT_TXT = "PARROT_v1_0_cleaned.txt"
OUTPUT_ENGLISH = "PARROT_v1_0_english_only.txt"
OUTPUT_POLISH = "PARROT_v1_0_polish_reports.txt"

# Define Polish-specific characters
POLISH_CHARS = {
    'ł': 'U+0142',  # L with stroke
    'ś': 'U+015B',  # S with acute
    'ę': 'U+0119',  # E with ogonek
    'ą': 'U+0105',  # A with ogonek
    'ó': 'U+00F3',  # O with acute
    'ż': 'U+017C',  # Z with dot above
    'ć': 'U+0107',  # C with acute
    'ń': 'U+0144',  # N with acute
}

def has_polish_chars(text):
    """
    Check if the text contains any Polish-specific characters.
    
    Args:
        text: String to check
        
    Returns:
        tuple: (has_polish, list of found Polish characters)
    """
    found_chars = []
    for char in POLISH_CHARS.keys():
        if char in text:
            found_chars.append(char)
    return (len(found_chars) > 0, found_chars)

def separate_polish_reports(input_file, output_english, output_polish):
    """
    Separate Polish reports from English reports.
    
    Args:
        input_file: Path to the input text file
        output_english: Path to save English-only reports
        output_polish: Path to save Polish reports
    """
    print(f"Reading from: {input_file}")
    print(f"\nPolish characters to detect:")
    for char, unicode in POLISH_CHARS.items():
        print(f"  {char} ({unicode})")
    print()
    
    # Read all lines
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_reports = len(lines)
    print(f"Total reports: {total_reports:,}\n")
    
    # Separate lines
    english_lines = []
    polish_lines = []
    polish_char_stats = {char: 0 for char in POLISH_CHARS.keys()}
    
    print("Processing reports...")
    for i, line in enumerate(lines, 1):
        has_polish, found_chars = has_polish_chars(line)
        
        if has_polish:
            polish_lines.append(line)
            # Count which Polish characters were found
            for char in found_chars:
                polish_char_stats[char] += 1
            
            # Show progress every 10 Polish reports
            if len(polish_lines) % 10 == 0:
                print(f"  Found {len(polish_lines)} Polish reports so far... (processing {i}/{total_reports})")
        else:
            english_lines.append(line)
    
    # Save English reports
    print(f"\nSaving English-only reports to: {output_english}")
    with open(output_english, 'w', encoding='utf-8') as f:
        f.writelines(english_lines)
    
    # Save Polish reports
    print(f"Saving Polish reports to: {output_polish}")
    with open(output_polish, 'w', encoding='utf-8') as f:
        f.writelines(polish_lines)
    
    # Calculate statistics
    english_count = len(english_lines)
    polish_count = len(polish_lines)
    english_chars = sum(len(line) for line in english_lines)
    polish_chars = sum(len(line) for line in polish_lines)
    
    # Print summary
    print(f"\n{'='*70}")
    print("SEPARATION SUMMARY")
    print("="*70)
    
    print(f"\nTotal reports processed: {total_reports:,}")
    print(f"\nEnglish-only reports: {english_count:,} ({english_count/total_reports*100:.2f}%)")
    print(f"  Total characters: {english_chars:,}")
    print(f"  Average length: {english_chars/english_count if english_count > 0 else 0:.1f} chars/report")
    
    print(f"\nPolish reports removed: {polish_count:,} ({polish_count/total_reports*100:.2f}%)")
    print(f"  Total characters: {polish_chars:,}")
    print(f"  Average length: {polish_chars/polish_count if polish_count > 0 else 0:.1f} chars/report")
    
    print(f"\nPolish character distribution in removed reports:")
    for char in sorted(polish_char_stats.keys(), key=lambda x: polish_char_stats[x], reverse=True):
        count = polish_char_stats[char]
        if count > 0:
            unicode_code = POLISH_CHARS[char]
            print(f"  {char} ({unicode_code}): found in {count} reports")
    
    print(f"\n{'='*70}")
    print("OUTPUT FILES")
    print("="*70)
    print(f"English corpus: {output_english}")
    print(f"  - {english_count:,} reports")
    print(f"  - {english_chars:,} characters")
    print(f"\nPolish reports (excluded): {output_polish}")
    print(f"  - {polish_count:,} reports")
    print(f"  - {polish_chars:,} characters")
    
    print(f"\n✓ Separation complete!")
    
    return english_count, polish_count

if __name__ == "__main__":
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Resolve paths
    input_path = os.path.join(script_dir, INPUT_TXT)
    output_english_path = os.path.join(script_dir, OUTPUT_ENGLISH)
    output_polish_path = os.path.join(script_dir, OUTPUT_POLISH)
    
    # Verify input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        exit(1)
    
    # Separate Polish reports
    english_count, polish_count = separate_polish_reports(
        input_path, 
        output_english_path, 
        output_polish_path
    )
