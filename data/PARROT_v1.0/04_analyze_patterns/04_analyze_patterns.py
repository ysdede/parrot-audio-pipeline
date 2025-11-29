"""
Analyze repeating string patterns in medical radiology reports.

This script:
1. Reads the normalized translations text file
2. Analyzes character and word n-grams to find repeating patterns
3. Identifies common phrases, headers, and structural elements
4. Outputs statistical analysis of the most frequent patterns
"""

import os
import re
from collections import Counter, defaultdict
import json

# Define input and output paths
INPUT_TXT = "../03_normalize_line_separators/PARROT_v1_0_translations_normalized.txt"
OUTPUT_DIR = "."

def extract_ngrams(text, n, use_words=True):
    """
    Extract n-grams from text.
    
    Args:
        text: Input text string
        n: Size of n-grams
        use_words: If True, use word-level n-grams; if False, use character-level
    
    Returns:
        List of n-grams
    """
    if use_words:
        # Split on whitespace and punctuation but keep structure
        tokens = re.findall(r'\b\w+\b', text)
        if len(tokens) < n:
            return []
        return [' '.join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
    else:
        # Character-level n-grams
        if len(text) < n:
            return []
        return [text[i:i+n] for i in range(len(text) - n + 1)]

def analyze_patterns(input_file, output_dir):
    """
    Analyze repeating patterns in the text file.
    
    Args:
        input_file: Path to the input text file
        output_dir: Directory to save analysis results
    """
    print(f"Reading from: {input_file}")
    
    # Read all translations
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    translations = [line.strip() for line in lines if line.strip()]
    print(f"Loaded {len(translations)} translations")
    
    # Combine all text for corpus-level analysis
    corpus = '\n'.join(translations)
    
    print(f"\nCorpus statistics:")
    print(f"  Total characters: {len(corpus):,}")
    print(f"  Total words: {len(corpus.split()):,}")
    print(f"  Total translations: {len(translations):,}")
    
    # Analyze different n-gram sizes
    results = {}
    
    # Word-level n-grams (for phrases)
    print("\n" + "="*60)
    print("Analyzing word-level n-grams (phrases)...")
    print("="*60)
    
    for n in [2, 3, 4, 5]:
        print(f"\nExtracting {n}-word phrases...")
        ngrams = []
        
        for translation in translations:
            ngrams.extend(extract_ngrams(translation, n, use_words=True))
        
        counter = Counter(ngrams)
        # Filter to only keep patterns that appear at least 3 times
        frequent_patterns = {k: v for k, v in counter.items() if v >= 3}
        
        print(f"  Found {len(ngrams):,} total {n}-grams")
        print(f"  Found {len(frequent_patterns):,} patterns appearing ≥3 times")
        
        # Store top 50
        results[f'{n}_word_ngrams'] = dict(counter.most_common(50))
    
    # Character-level n-grams (for shorter patterns)
    print("\n" + "="*60)
    print("Analyzing character-level n-grams...")
    print("="*60)
    
    for n in [10, 15, 20]:
        print(f"\nExtracting {n}-character patterns...")
        ngrams = []
        
        for translation in translations:
            ngrams.extend(extract_ngrams(translation, n, use_words=False))
        
        counter = Counter(ngrams)
        # Filter to only keep patterns that appear at least 5 times
        frequent_patterns = {k: v for k, v in counter.items() if v >= 5}
        
        print(f"  Found {len(ngrams):,} total {n}-grams")
        print(f"  Found {len(frequent_patterns):,} patterns appearing ≥5 times")
        
        # Store top 30
        results[f'{n}_char_ngrams'] = dict(counter.most_common(30))
    
    # Find common headers/section markers (lines that start translations)
    print("\n" + "="*60)
    print("Analyzing common headers/starting phrases...")
    print("="*60)
    
    # Extract first 50 characters of each translation
    headers = [trans[:50] for trans in translations if len(trans) >= 10]
    header_counter = Counter(headers)
    results['common_headers'] = dict(header_counter.most_common(30))
    print(f"  Found {len(header_counter)} unique headers")
    
    # Save detailed results to JSON
    output_json = os.path.join(output_dir, "pattern_analysis.json")
    print(f"\nSaving detailed results to: {output_json}")
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Create human-readable report
    output_report = os.path.join(output_dir, "pattern_analysis_report.txt")
    print(f"Saving human-readable report to: {output_report}")
    
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write("MEDICAL RADIOLOGY REPORTS - PATTERN ANALYSIS\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Corpus Statistics:\n")
        f.write(f"  Total translations: {len(translations):,}\n")
        f.write(f"  Total characters: {len(corpus):,}\n")
        f.write(f"  Total words: {len(corpus.split()):,}\n\n")
        
        # Word n-grams
        for n in [2, 3, 4, 5]:
            f.write(f"\n{'='*70}\n")
            f.write(f"TOP 20 MOST COMMON {n}-WORD PHRASES\n")
            f.write(f"{'='*70}\n\n")
            
            key = f'{n}_word_ngrams'
            if key in results:
                for i, (pattern, count) in enumerate(list(results[key].items())[:20], 1):
                    f.write(f"{i:3}. [{count:5}x] {pattern}\n")
        
        # Character n-grams
        for n in [10, 15, 20]:
            f.write(f"\n{'='*70}\n")
            f.write(f"TOP 15 MOST COMMON {n}-CHARACTER PATTERNS\n")
            f.write(f"{'='*70}\n\n")
            
            key = f'{n}_char_ngrams'
            if key in results:
                for i, (pattern, count) in enumerate(list(results[key].items())[:15], 1):
                    # Escape newlines for display
                    display_pattern = pattern.replace('\n', '\\n')
                    f.write(f"{i:3}. [{count:5}x] {display_pattern}\n")
        
        # Common headers
        f.write(f"\n{'='*70}\n")
        f.write(f"TOP 20 MOST COMMON HEADERS (first 50 chars)\n")
        f.write(f"{'='*70}\n\n")
        
        if 'common_headers' in results:
            for i, (header, count) in enumerate(list(results['common_headers'].items())[:20], 1):
                display_header = header.replace('\n', '\\n')
                f.write(f"{i:3}. [{count:5}x] {display_header}...\n")
    
    print(f"\n✓ Pattern analysis complete!")
    print(f"\nFiles created:")
    print(f"  - {output_json}")
    print(f"  - {output_report}")

if __name__ == "__main__":
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Resolve paths
    input_path = os.path.join(script_dir, INPUT_TXT)
    output_dir = script_dir
    
    # Verify input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        exit(1)
    
    # Analyze patterns
    analyze_patterns(input_path, output_dir)
