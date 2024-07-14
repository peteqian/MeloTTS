import csv
import os

# Define the input and output file paths
input_file = 'thorsten-de_v03/metadata.csv'
output_file = 'data/de/metadata.list'

# Define constants
speaker_name = 'thorsten-de'
language_code = 'DE'
# audio_directory = 'data/example/wavs/'
audio_directory = 'thorsten-de_v03/wavs/'

# Ensure the output directory exists
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to process each row
def process_row(row):
    parts = row[0].split('|')
    if len(parts) != 2:
        raise ValueError(f"Invalid format in row: {row}")
    audio_id, text = parts
    audio_filename = f"{audio_directory}{audio_id}.wav"
    new_line = f"{audio_filename}|{speaker_name}|{language_code}|{text}"
    return new_line

# Read the input file and process each row
with open(input_file, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    lines = list(reader)

# Process rows and write to output file
with open(output_file, 'w', encoding='utf-8') as outfile:
    for index, row in enumerate(lines):
        new_line = process_row(row)
        outfile.write(new_line + '\n')

print(f"Conversion complete. Output written to {output_file}")