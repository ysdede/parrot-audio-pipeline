import json
import csv
import os

# Configuration
INPUT_FILE = r"sources\PARROT_v1.0\data\PARROT_v1_0.jsonl"
OUTPUT_FILE = r"sources\PARROT_v1.0\data\PARROT_v1_0_escaped.csv"

def convert_jsonl_to_csv(input_path, output_path):
    # Resolve absolute paths
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)

    print(f"Reading from: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    data = []
    headers = set()
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    try:
                        item = json.loads(line)
                        data.append(item)
                        headers.update(item.keys())
                    except json.JSONDecodeError as e:
                        print(f"Warning: Could not parse JSON on line {line_num}: {e}")
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Sort headers for consistent output
    # Prioritize 'no' as the first column if it exists
    sorted_headers = sorted(list(headers))
    if 'no' in sorted_headers:
        sorted_headers.remove('no')
        sorted_headers.insert(0, 'no')

    print(f"Found {len(data)} records.")
    print(f"Detected headers: {sorted_headers}")
    
    # Pre-process data to escape newlines
    print("Escaping newlines in data...")
    processed_data = []
    for row in data:
        new_row = {}
        for k, v in row.items():
            if isinstance(v, str):
                # Replace actual newlines with literal \n sequence
                new_row[k] = v.replace('\n', '\\n').replace('\r', '\\r')
            else:
                new_row[k] = v
        processed_data.append(new_row)
    
    print(f"Writing to: {output_path}")
    try:
        # Using utf-8-sig for better Excel compatibility with non-ASCII characters
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            # quote_all ensures newlines and special chars in fields are properly escaped/quoted
            writer = csv.DictWriter(f, fieldnames=sorted_headers, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(processed_data)
        print("Conversion complete successfully.")
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    convert_jsonl_to_csv(INPUT_FILE, OUTPUT_FILE)
