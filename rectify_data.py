import json

# File paths
input_file_path = "new_data.jsonl"  # Change this to the location of your raw data file
output_file_path = "rectified_data.json"  # This is where your corrected JSON file will be saved

def rectify_data():
    with open(input_file_path, "r") as f:
        # Read the file
        raw_data = f.read()

    # Split entries by assuming each entry starts with '{"instruction"'
    data_entries = raw_data.split('{"instruction"')
    
    # Reconstruct valid JSON objects by adding back '{"instruction"'
    json_list = []
    for entry in data_entries[1:]:  # Skipping the first empty split
        # Add back the removed part
        entry = '{"instruction"' + entry.strip()  # Stripping white spaces
        
        # Fix missing commas between elements (if needed)
        if not entry.endswith('}'):
            entry += '}'  # Ensure each entry ends correctly
        
        try:
            # Try parsing to ensure it's valid JSON
            json_obj = json.loads(entry)
            json_list.append(json_obj)
        except json.JSONDecodeError:
            print(f"Skipping invalid entry: {entry}")

    # Save the corrected list of JSON objects to a file
    with open(output_file_path, "w") as out_file:
        json.dump(json_list, out_file, indent=4)
    
    print(f"Data rectified and saved to {output_file_path}")

if __name__ == "__main__":
    rectify_data()