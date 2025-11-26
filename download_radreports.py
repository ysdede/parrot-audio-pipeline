import os
import requests
import json
import time

# Configuration
BASE_URL = "https://api3.rsna.org/radreport/v1"
OUTPUT_DIR = os.path.join("sources", "radreport.org")
LANGUAGE = "en"

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")

def get_templates(language="en"):
    url = f"{BASE_URL}/templates"
    params = {
        "language": language,
        "limit": 10000  # Set a high limit to get all templates, or handle pagination if needed
    }
    print(f"Fetching templates list from {url}...")
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        # The API might return a list directly or a dict with a list under a key like 'DATA' or 'templates'
        # Based on typical REST APIs, let's inspect the structure. 
        # If it's a list, return it. If it's a dict, look for the list.
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            # Common keys for list wrappers
            for key in ['DATA', 'data', 'templates', 'results']:
                if key in data:
                    return data[key]
            return [data] # fallback
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching templates: {e}")
        return []

def get_template_details(template_id):
    url = f"{BASE_URL}/templates/{template_id}/details"
    print(f"Fetching details for template ID: {template_id}...")
    try:
        response = requests.get(url)
        data = response.json()
        if isinstance(data, dict) and 'DATA' in data:
            return data['DATA']
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching details for template {template_id}: {e}")
        return None

def save_report(report_data, output_dir):
    # Extract ID and Title for filename
    # Adjust keys based on actual API response structure
    template_id = report_data.get("templateId", report_data.get("id", report_data.get("template_id")))
    
    if not template_id:
        print(f"Warning: Could not find ID in report data. Keys: {list(report_data.keys())}")
        template_id = "unknown_id"
    title = report_data.get("title", "untitled").replace("/", "-").replace("\\", "-") # Sanitize title
    
    filename = f"{template_id}.json"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)
    print(f"Saved: {filepath}")

def main():
    create_directory(OUTPUT_DIR)
    
    templates = get_templates(LANGUAGE)
    print(f"Found {len(templates)} templates.")
    
    for template in templates:
        # The list endpoint might return a simplified object. 
        # We need the ID to get full details.
        # API returns 'template_id' based on the logs
        template_id = template.get("templateId", template.get("id", template.get("template_id")))
        
        if template_id:
            details = get_template_details(template_id)
            if details:
                save_report(details, OUTPUT_DIR)
            
            # Be nice to the API
            time.sleep(0.1) 
        else:
            print(f"Could not find ID for template: {template}")

if __name__ == "__main__":
    main()
