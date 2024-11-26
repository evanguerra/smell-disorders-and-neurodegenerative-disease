import re
from transformers import AutoTokenizer
import numpy

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")


# Helper function to split PubTator annotations and text
def parse_pubtator_file(file_path):
    with open(file_path, 'r') as f:
        raw_data = f.read().strip().split('\n\n')

    data = []
    for block in raw_data:
        lines = block.split('\n')
        pmid, title_line = lines[0].split('|')[0], lines[0]
        abstract_line = lines[1]
        annotations = lines[2:]  # List of entity annotations

        # Collect the text (title + abstract)
        title = title_line.split('|')[2]
        abstract = abstract_line.split('|')[2]
        full_text = title + " " + abstract

        # Collect annotations in tuples: (start, end, entity_type)
        entity_info = []
        for annotation in annotations:
            parts = annotation.split('\t')
            entity_info.append((int(parts[1]), int(parts[2]), parts[4]))

        data.append((full_text, entity_info))

    return data


# Function to convert PubTator data into tokenized BIO format
def convert_to_bio_format(data):
    bio_data = []

    for text, entities in data:
        # Tokenize the text
        tokens = tokenizer.tokenize(text)
        token_offsets = tokenizer(text, return_offsets_mapping=True)['offset_mapping']

        # Initialize BIO labels
        labels = ['O'] * len(tokens)

        # Assign BIO labels based on entity annotations
        for start, end, entity_type in entities:
            for i, (token_start, token_end) in enumerate(token_offsets):
                if token_start >= start and token_end <= end:
                    if token_start == start:
                        labels[i] = f'B-{entity_type}'
                    else:
                        labels[i] = f'I-{entity_type}'

        # Combine tokenized words with their BIO labels
        bio_data.append(list(zip(tokens, labels)))

    return bio_data


# Write BIO-formatted data to a file
def write_bio_file(bio_data, output_file):
    with open(output_file, 'w') as f:
        for sentence in bio_data:
            for token, label in sentence:
                f.write(f"{token}\t{label}\n")
            f.write("\n")  # Separate sentences by a blank line


# File path to your PubTator data
pubtator_file = 'neurodegenerative-disease/output_subset.txt'

# Process PubTator data
data = parse_pubtator_file(pubtator_file)

# Convert data to BIO format
bio_data = convert_to_bio_format(data)

# Save the BIO format data to a .txt file
write_bio_file(bio_data, 'neurodegenerative-disease/bio_format_output.txt')

print("Data has been converted to BIO format and saved to 'bio_format_output.txt'.")
