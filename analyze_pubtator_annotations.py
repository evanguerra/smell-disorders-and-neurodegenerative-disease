import spacy
import re
from collections import defaultdict

# Load a SpaCy model
nlp = spacy.load("en_core_web_sm")


def parse_pubtator_file(file_path):
    data = {}

    # Read the contents of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        pubtator_text = file.read()

    # Split the input into lines for processing
    lines = pubtator_text.strip().split('\n')

    # Initialize counters and structures for the summary
    pmids = set()  # To store unique PMIDs
    tokens_count = 0
    sentences_count = 0
    entities_count = 0
    relations_count = 0
    entities_by_type = defaultdict(int)
    relations_by_type = defaultdict(int)

    current_abstract = None

    # Iterate through the lines to extract titles, abstracts, and annotations
    for line in lines:
        if '\t' not in line:  # This is an empty line or header
            continue

        # Handle abstracts
        if '|a|' in line:
            pmid, _, abstract = line.partition('|a|')
            pmid = pmid.strip()
            abstract = abstract.strip()
            pmids.add(pmid)  # Add PMID to the set for unique count

            # Process the abstract with SpaCy
            doc = nlp(abstract)
            tokens_count += len(doc)  # Count tokens
            sentences_count += len(list(doc.sents))  # Count sentences

            current_abstract = abstract  # Store the current abstract for future use
            continue

        # Handle annotations (tab-separated)
        parts = line.split('\t')

        if len(parts) >= 5:  # Expecting at least PMID, start, end, entity, entity type
            entity_type = parts[4].strip()
            entities_count += 1  # Increment total entity count
            entities_by_type[entity_type] += 1  # Increment specific entity type count

        # Handle relations
        elif len(parts) >= 3:  # Expecting at least PMID, relation type, and at least one more part
            if parts[1].strip():  # Check if the relation type is not empty
                relation_type = parts[1].strip()
                relations_count += 1  # Increment total relation count
                relations_by_type[relation_type] += 1  # Increment specific relation type count

    # Prepare the final data summary
    summary = {
        'Total Articles': len(pmids),
        'Total Tokens': tokens_count,
        'Total Sentences': sentences_count,
        'Total Entities': entities_count,
        'Total Relations': relations_count,
        'Entities by Type': dict(entities_by_type),
        'Relations by Type': dict(relations_by_type)
    }

    return summary

# Example usage
file_path = 'neurodegenerative-disease/SessionNumber.txt'  # Update with the actual file path
parsed_data = parse_pubtator_file(file_path)
print(parsed_data)
