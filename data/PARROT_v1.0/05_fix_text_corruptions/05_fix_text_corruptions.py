"""
Fix text corruptions in the medical radiology reports.

This script:
1. Removes Private Use Area (PUA) corrupted characters
2. Normalizes whitespace (non-breaking spaces, zero-width spaces, tabs)
3. Normalizes typography (smart quotes, dashes, bullets)
4. Cleans up multiple consecutive spaces
5. Reports all changes made
"""

import os
import re

# Define input and output paths
INPUT_TXT = "../03_normalize_line_separators/PARROT_v1_0_translations_normalized.txt"
OUTPUT_TXT = "PARROT_v1_0_cleaned.txt"

def fix_corruptions(input_file, output_file):
    """
    Fix text corruptions and normalize characters.
    
    Args:
        input_file: Path to the input text file
        output_file: Path to save the cleaned text file
    """
    print(f"Reading from: {input_file}")
    
    # Read the entire file
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    original_length = len(text)
    print(f"Original file size: {original_length:,} characters\n")
    
    # Track changes
    changes = {}
    
    # 1. REMOVE PRIVATE USE AREA (PUA) CORRUPTED CHARACTERS
    print("="*70)
    print("STEP 1: Removing Private Use Area (PUA) corrupted characters")
    print("="*70)
    
    pua_replacements = {
        '\uF06C': ' ',  # Replace with space to avoid merging words
        '\uF0D8': ' ',
        '\uF076': ' ',
        '\uF06E': ' ',
    }
    
    for char, replacement in pua_replacements.items():
        count = text.count(char)
        if count > 0:
            text = text.replace(char, replacement)
            changes[f'PUA {repr(char)}'] = count
            print(f"  Removed {count}x {repr(char)} (U+{ord(char):04X})")
    
    # 2. NORMALIZE WHITESPACE
    print(f"\n{'='*70}")
    print("STEP 2: Normalizing whitespace characters")
    print("="*70)
    
    whitespace_replacements = {
        '\u00A0': ' ',   # Non-breaking space → regular space
        '\u200B': '',    # Zero-width space → remove
        '\u0009': ' ',   # Tab → regular space
    }
    
    for char, replacement in whitespace_replacements.items():
        count = text.count(char)
        if count > 0:
            text = text.replace(char, replacement)
            changes[f'Whitespace {repr(char)}'] = count
            action = "removed" if replacement == '' else "normalized"
            print(f"  {action.capitalize()} {count}x {repr(char)} (U+{ord(char):04X})")
    
    # 3. NORMALIZE TYPOGRAPHY
    print(f"\n{'='*70}")
    print("STEP 3: Normalizing typography")
    print("="*70)
    
    typography_replacements = {
        '\u2013': '-',   # En-dash → hyphen
        '\u2014': '-',   # Em-dash → hyphen
        '\u2019': "'",   # Smart apostrophe → straight quote
        '\u201C': '"',   # Left smart quote → straight quote
        '\u201D': '"',   # Right smart quote → straight quote
        '\u2022': '-',   # Bullet → hyphen
    }
    
    for char, replacement in typography_replacements.items():
        count = text.count(char)
        if count > 0:
            text = text.replace(char, replacement)
            changes[f'Typography {repr(char)}'] = count
            print(f"  Normalized {count}x {repr(char)} (U+{ord(char):04X}) → {repr(replacement)}")
    
    # 4. CLEAN UP MULTIPLE CONSECUTIVE SPACES
    print(f"\n{'='*70}")
    print("STEP 4: Cleaning up multiple consecutive spaces")
    print("="*70)
    
    # Count spaces before cleanup
    multi_space_pattern = re.compile(r' {2,}')
    multi_spaces = multi_space_pattern.findall(text)
    multi_space_count = len(multi_spaces)
    
    if multi_space_count > 0:
        # Replace multiple spaces with single space
        text = multi_space_pattern.sub(' ', text)
        changes['Multiple spaces'] = multi_space_count
        print(f"  Cleaned up {multi_space_count} instances of multiple consecutive spaces")
    else:
        print(f"  No multiple consecutive spaces found")
    
    # Save the cleaned text
    print(f"\n{'='*70}")
    print("SAVING CLEANED TEXT")
    print("="*70)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    final_length = len(text)
    chars_removed = original_length - final_length
    
    print(f"Writing to: {output_file}")
    print(f"\nFinal file size: {final_length:,} characters")
    print(f"Characters removed: {chars_removed:,}")
    print(f"Compression: {(chars_removed/original_length)*100:.2f}%")
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY OF CHANGES")
    print("="*70)
    
    total_changes = sum(changes.values())
    print(f"\nTotal replacements made: {total_changes:,}\n")
    
    if changes:
        print("Breakdown by category:")
        for category, count in sorted(changes.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count:,}")
    
    print(f"\n✓ Text cleaning complete!")

if __name__ == "__main__":
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Resolve paths
    input_path = os.path.join(script_dir, INPUT_TXT)
    output_path = os.path.join(script_dir, OUTPUT_TXT)
    
    # Verify input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        exit(1)
    
    # Fix corruptions
    fix_corruptions(input_path, output_path)
