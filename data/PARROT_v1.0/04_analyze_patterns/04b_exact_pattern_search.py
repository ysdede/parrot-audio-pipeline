"""
Search for exact string patterns in the corpus with accurate counts.

This script:
1. Reads the normalized translations
2. Searches for exact pattern matches (case-sensitive and case-insensitive)
3. Handles escaped newlines properly
4. Provides accurate occurrence counts
"""

import os
import re
from collections import Counter

# Define input path
INPUT_TXT = "../03_normalize_line_separators/PARROT_v1_0_translations_normalized.txt"
OUTPUT_TXT = "exact_pattern_counts.txt"

def search_exact_patterns(input_file, output_file):
    """
    Search for exact patterns and count their occurrences.
    
    Args:
        input_file: Path to the input text file
        output_file: Path to save the results
    """
    print(f"Reading from: {input_file}")
    
    # Read the entire corpus
    with open(input_file, 'r', encoding='utf-8') as f:
        corpus = f.read()
    
    # Also read line by line to count per-translation
    with open(input_file, 'r', encoding='utf-8') as f:
        translations = [line.strip() for line in f.readlines() if line.strip()]
    
    print(f"Loaded {len(translations)} translations")
    print(f"Total corpus size: {len(corpus):,} characters\n")
    
    # Define patterns to search for (add more as needed)
    search_patterns = [
        "Description and Findings",
        "Posterior Fossa",
        "Fourth Ventricle",
        "Brainstem",
        "Cerebellum",
        "Unremarkable",
        "Normal shape and size",
        "No evidence of",
        "within normal limits",
        "Imaging Comment",
        "Diagnostic Impression",
        "CONCLUSION",
        "Indication:",
        "Technique:",
        "Clinical Information",
        "The examination was performed",
        "MRI",
        "CT",
        "Alignment: preserved",
        "height and signal preserved",
    ]
    
    results = []
    
    print("="*70)
    print("SEARCHING FOR EXACT PATTERNS")
    print("="*70)
    
    for pattern in search_patterns:
        # Case-sensitive search
        count_sensitive = corpus.count(pattern)
        
        # Case-insensitive search
        count_insensitive = len(re.findall(re.escape(pattern), corpus, re.IGNORECASE))
        
        # Count how many translations contain this pattern
        translations_with_pattern = sum(1 for t in translations if pattern in t)
        
        # Count how many translations contain this pattern (case-insensitive)
        translations_with_pattern_ci = sum(1 for t in translations if pattern.lower() in t.lower())
        
        results.append({
            'pattern': pattern,
            'count_case_sensitive': count_sensitive,
            'count_case_insensitive': count_insensitive,
            'translations_with_pattern': translations_with_pattern,
            'translations_with_pattern_ci': translations_with_pattern_ci
        })
        
        print(f"\nPattern: '{pattern}'")
        print(f"  Case-sensitive count:     {count_sensitive:4} occurrences")
        print(f"  Case-insensitive count:   {count_insensitive:4} occurrences")
        print(f"  In # translations (CS):   {translations_with_pattern:4} / {len(translations)}")
        print(f"  In # translations (CI):   {translations_with_pattern_ci:4} / {len(translations)}")
    
    # Write results to file
    print(f"\n{'='*70}")
    print(f"Writing results to: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("EXACT PATTERN SEARCH RESULTS\n")
        f.write("="*70 + "\n\n")
        f.write(f"Corpus size: {len(corpus):,} characters\n")
        f.write(f"Total translations: {len(translations):,}\n\n")
        
        f.write("="*70 + "\n")
        f.write("PATTERN OCCURRENCE COUNTS\n")
        f.write("="*70 + "\n\n")
        
        # Sort by case-insensitive count
        sorted_results = sorted(results, key=lambda x: x['count_case_insensitive'], reverse=True)
        
        for r in sorted_results:
            f.write(f"\nPattern: '{r['pattern']}'\n")
            f.write(f"  Total occurrences (case-sensitive):     {r['count_case_sensitive']:5}\n")
            f.write(f"  Total occurrences (case-insensitive):   {r['count_case_insensitive']:5}\n")
            f.write(f"  Appears in N translations (CS):         {r['translations_with_pattern']:5} / {len(translations)} ({r['translations_with_pattern']/len(translations)*100:.1f}%)\n")
            f.write(f"  Appears in N translations (CI):         {r['translations_with_pattern_ci']:5} / {len(translations)} ({r['translations_with_pattern_ci']/len(translations)*100:.1f}%)\n")
    
    # Now let's also find ALL phrases that appear more than 20 times
    print(f"\n{'='*70}")
    print("FINDING ALL MULTI-WORD PHRASES WITH 20+ OCCURRENCES")
    print("="*70)
    
    # Extract all phrases of 3-6 words
    all_phrases = []
    for translation in translations:
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
    
    print(f"Found {len(frequent_phrases)} phrases appearing 20+ times")
    
    # Add to output file
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write("\n\n" + "="*70 + "\n")
        f.write("TOP 100 PHRASES APPEARING 20+ TIMES\n")
        f.write("="*70 + "\n\n")
        
        for i, (phrase, count) in enumerate(frequent_phrases[:100], 1):
            f.write(f"{i:3}. [{count:4}x] {phrase}\n")
    
    print(f"\n✓ Exact pattern search complete!")
    print(f"Results saved to: {output_file}")

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
    
    # Search for patterns
    search_exact_patterns(input_path, output_path)
