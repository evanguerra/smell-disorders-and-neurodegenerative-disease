import spacy
from collections import defaultdict, Counter

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

    # Counters for specific IDs and tracking of smell words in articles with specific IDs
    target_ids = {
        'MESH:D000544': 0,
        'MESH:C537240': 0,
        'MESH:D003704': 0,
        'MESH:D019636': 0,
        'MESH:D010300': 0,
        'MESH:D000857': 0
    }
    smell_entity_words = Counter()
    neurodegenerative_smell_cooccurrence = defaultdict(lambda: defaultdict(Counter))

    current_abstract = None
    current_pmid = None
    neuro_ids_in_article = set()  # Tracks neurodegenerative IDs in each article for co-occurrence

    # Iterate through the lines to extract titles, abstracts, and annotations
    for line in lines:
        if '\t' not in line:  # Empty line or header
            continue

        # Handle abstracts
        if '|a|' in line:
            pmid, _, abstract = line.partition('|a|')
            pmid = pmid.strip()
            abstract = abstract.strip()
            pmids.add(pmid)  # Add PMID to the set for unique count
            current_pmid = pmid  # Track the current PMID for co-occurrences

            # Process the abstract with SpaCy
            doc = nlp(abstract)
            tokens_count += len(doc)  # Count tokens
            sentences_count += len(list(doc.sents))  # Count sentences

            current_abstract = abstract  # Store the current abstract for future use
            neuro_ids_in_article.clear()  # Reset for each article
            continue

        # Handle annotations (tab-separated)
        parts = line.split('\t')

        if len(parts) >= 6:  # Entity lines with sufficient fields
            entity_id = parts[5].strip()
            entity_type = parts[4].strip()
            entities_count += 1  # Increment total entity count
            entities_by_type[entity_type] += 1  # Increment specific entity type count

            # Increment counts for target IDs and track for co-occurrences
            if entity_id in target_ids:
                target_ids[entity_id] += 1

                # Track neurodegenerative disease IDs and smell disorder entities
                if entity_id in {'MESH:D000544', 'MESH:C537240', 'MESH:D003704', 'MESH:D019636', 'MESH:D010300'}:
                    neuro_ids_in_article.add(entity_id)  # Track neurodegenerative disease ID in this article

                # Track smell disorder entities and record co-occurrences
                elif entity_id == 'MESH:D000857':
                    smell_word = parts[3].strip().lower()  # Convert to lowercase
                    smell_entity_words[smell_word] += 1

                    # Check if any neurodegenerative IDs are in this article, indicating co-occurrence
                    for neuro_id in neuro_ids_in_article:
                        neurodegenerative_smell_cooccurrence[neuro_id][smell_word][current_pmid] += 1

    # Sort smell entity words by frequency, most to least frequent
    sorted_smell_entity_words = dict(smell_entity_words.most_common())

    # Prepare co-occurrence summary for readability
    co_occurrence_summary = {
        neuro_id: {smell_word: count for smell_word, pmids in words.items() for count in pmids.values()}
        for neuro_id, words in neurodegenerative_smell_cooccurrence.items()
    }

    # Prepare the final data summary
    summary = {
        #'Total Articles': len(pmids),
        #'Total Tokens': tokens_count,
        #'Total Sentences': sentences_count,
        #'Total Entities': entities_count,
        #'Total Relations': relations_count,
        #'Entities by Type': dict(entities_by_type),
        #'Relations by Type': dict(relations_by_type),
        #'Target ID Counts': dict(target_ids),
        #'Smell Disorder Entity Words': sorted_smell_entity_words,
        'Co-Occurrences': co_occurrence_summary
    }

    return summary

# Example usage
file_path = 'SessionNumber.txt'  # Update with the actual file path
parsed_data = parse_pubtator_file(file_path)
print(parsed_data)
