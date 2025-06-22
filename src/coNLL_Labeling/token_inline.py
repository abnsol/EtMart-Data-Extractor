import os
import re

input_file_name = "labeled_data_conll.txt"
file_to_process = os.path.join('data', 'output_data', 'processed_for_labeling', input_file_name)

token_pattern = re.compile(r"'(.*?)'")  # matches all 'token' strings

with open(file_to_process, 'r', encoding='utf-8') as file:
    for line_num, line in enumerate(file, 1):
        line = line.strip()
        if not line:
            continue
        try:
            tokens = token_pattern.findall(line)
            for token in tokens:
                print(token)
            print()
            print()
        except Exception as e:
            print(f"Error parsing line {line_num}: {e}")
