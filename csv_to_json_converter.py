import csv
import json
from pathlib import Path

def csv_to_json(input_path, output_path="output.json"):
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"Error: File '{input_path}' not found.")
        return

    try:
        with open(input_file, 'r', encoding='utf-8', newline='') as f:
            # Check if file is empty
            sample = f.read(2048)
            if not sample.strip():
                print("Error: The file is empty.")
                return
            
            # Reset file pointer to start after reading sample
            f.seek(0)
            
            # Auto-detect delimiter
            try:
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(sample, delimiters=',\t;|')
            except csv.Error:
                # Fallback to comma if sniffing fails
                dialect = csv.excel 

            # Read CSV and convert to list of dictionaries
            reader = csv.DictReader(f, dialect=dialect)
            data = [row for row in reader]

        # Save to JSON
        with open(output_path, 'w', encoding='utf-8') as json_f:
            json.dump(data, json_f, indent=4)
            
        print(f"Successfully converted {input_file.name} to {output_path}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


csv_to_json("data_for_csv_to_json.csv")
csv_to_json("data_for_csv_to_json2.csv")
