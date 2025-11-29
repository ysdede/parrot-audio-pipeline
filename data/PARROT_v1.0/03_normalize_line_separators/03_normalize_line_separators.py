"""
Normalize line separators in the translations text file.

This script:
1. Reads the plain text translations file
2. Converts Unicode Line Separator (U+2028) to escaped newline (\n)
3. Ensures consistent line separator usage
4. Saves the normalized text to a new file
"""

import os

# Define input and output paths
INPUT_TXT = "../02_extract_translation_column/PARROT_v1_0_translations.txt"
OUTPUT_TXT = "PARROT_v1_0_translations_normalized.txt"

def normalize_line_separators(input_file, output_file):
    """
    Normalize line separators by converting U+2028 to escaped \n.
    
    Args:
        input_file: Path to the input text file
        output_file: Path to the output normalized text file
    """
    print(f"Reading from: {input_file}")
    
    # Read the file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count occurrences before normalization
    u2028_count = content.count('\u2028')
    escaped_newline_count = content.count('\\n')
    
    print(f"\nBefore normalization:")
    print(f"  U+2028 (Line Separator): {u2028_count}")
    print(f"  Escaped \\n: {escaped_newline_count}")
    
    # Replace U+2028 (Line Separator) with escaped newline
    # U+2028 is a Unicode line separator character
    normalized_content = content.replace('\u2028', '\\n')
    
    # Count occurrences after normalization
    u2028_count_after = normalized_content.count('\u2028')
    escaped_newline_count_after = normalized_content.count('\\n')
    
    print(f"\nAfter normalization:")
    print(f"  U+2028 (Line Separator): {u2028_count_after}")
    print(f"  Escaped \\n: {escaped_newline_count_after}")
    print(f"  Converted: {u2028_count} U+2028 → \\n")
    
    # Write the normalized content
    print(f"\nWriting to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(normalized_content)
    
    # Get file sizes
    input_size = os.path.getsize(input_file)
    output_size = os.path.getsize(output_file)
    
    print(f"\nFile sizes:")
    print(f"  Input:  {input_size:,} bytes")
    print(f"  Output: {output_size:,} bytes")
    print(f"  Difference: {output_size - input_size:+,} bytes")
    
    print(f"\n✓ Successfully normalized line separators!")

if __name__ == "__main__":
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Resolve paths relative to script location
    input_path = os.path.join(script_dir, INPUT_TXT)
    output_path = os.path.join(script_dir, OUTPUT_TXT)
    
    # Verify input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        exit(1)
    
    # Normalize line separators
    normalize_line_separators(input_path, output_path)
