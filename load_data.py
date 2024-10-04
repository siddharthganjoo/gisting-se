import pandas as pd
import json
import subprocess
import difflib
from tqdm import tqdm  # Progress bar

# Function to run the compress.py script
def run_compress(instruction):
    cmd = [
        "python", "-m", "src.compress",
        "--model_name_or_path", "/home/sganjoo/gisting/llama-7b",
        "--instruction", instruction
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output_lines = result.stdout.split('\n')
    compression_factor = None
    predicted_code = None

    for line in output_lines:
        if "compression factor" in line:
            compression_factor_str = line.split(': ')[-1].replace('x', '').replace(')', '').strip()
            compression_factor = float(compression_factor_str)
        if "Output:" in line:
            predicted_code = '\n'.join(output_lines[output_lines.index(line) + 1:])
            break

    return compression_factor, predicted_code

# Function to calculate pass@k metric
def pass_k_metric(predicted_code, ground_truth, k):
    similarity = difflib.SequenceMatcher(None, predicted_code, ground_truth).ratio()
    return similarity >= 0.9  # Consider a match if similarity is above 90%

# Sanitize code for Excel
def sanitize_code_for_excel(code_str):
    return code_str.replace('\r', '')

# Function to process the dataset and generate an XLSX file with 50 prompts and pass@k
def generate_xlsx_for_excel(dataset_path, xlsx_output_path, k_values=[1, 3, 5]):
    # Load the dataset
    with open(dataset_path, 'r') as f:
        dataset = [json.loads(line) for line in f]

    # Collect data in a list for DataFrame
    data = []

    # Process the first 50 prompts
    for prompt in tqdm(dataset[:50], desc="Processing prompts"):
        instruction = prompt['instruction']
        ground_truth = sanitize_code_for_excel(prompt['output'])

        try:
            # Run compress.py for this instruction
            compression_factor, predicted_code = run_compress(instruction)
            predicted_code = sanitize_code_for_excel(predicted_code)

            # Calculate pass@k metrics
            pass_k_results = {f'pass@{k}': pass_k_metric(predicted_code, ground_truth, k) for k in k_values}

            # Add result to data list
            data.append({
                'original_prompt': instruction,
                'compression_factor': compression_factor,
                'groundTruth': ground_truth,
                'predicted_code': predicted_code,
                **pass_k_results  # Add pass@k results
            })

            print(f"Processed: {instruction}")

        except Exception as e:
            print(f"Error processing instruction: {instruction}")
            print(f"Error: {e}")

    # Create DataFrame
    df = pd.DataFrame(data)

    # Write DataFrame to XLSX
    df.to_excel(xlsx_output_path, index=False)

if __name__ == "__main__":
    # Path to the dataset file
    dataset_path = "/home/sganjoo/gisting/new_data.jsonl"

    # Path to save the XLSX file
    xlsx_output_path = "output_compressed_with_passk.xlsx"

    # Call the function to generate XLSX file for 50 prompts
    generate_xlsx_for_excel(dataset_path, xlsx_output_path)