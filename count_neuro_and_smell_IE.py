import spacy
from collections import defaultdict

# Load a SpaCy model
nlp = spacy.load("en_core_web_sm")


def parse_pubtator_file(file_path, output_file_path):
    data = {}

    # Read the contents of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        pubtator_text = file.read()

    # Split the input into articles for processing (separated by double newlines)
    articles = pubtator_text.strip().split('\n\n')

    # Initialize counters and structures for the summary
    pmids = set()  # To store unique PMIDs
    neurodegenerative_pmids = set()  # To store unique PMIDs with neurodegenerative diseases
    smell_disorder_pmids = set()  # To store unique PMIDs with smell disorders
    both_pmids = set()  # To store PMIDs with both neurodegenerative and smell disorder
    relations = []  # To store relations between neurodegenerative diseases and smell disorders

    # This will hold the counts of relations by type
    relation_counts = defaultdict(int)

    neurodegenerative_ids = {
        'MESH:D000544', 'MESH:C537240', 'MESH:D003704', 'MESH:D019636', 'MESH:D010300'
    }
    smell_disorder_id = 'MESH:D000857'

    # Initialize counters for total entities
    total_neurodegenerative_entities = 0
    total_smell_disorder_entities = 0

    # Initialize a list to hold articles containing both entities
    both_entities_articles = []

    # Iterate through the articles
    for article in articles:
        lines = article.strip().split('\n')  # Split the article into lines
        current_abstract = None

        for line in lines:
            if '|a|' in line:  # Check for the abstract line
                pmid, _, abstract = line.partition('|a|')
                pmid = pmid.strip()
                pmids.add(pmid)  # Add PMID to the set for unique count

                # Set flags for current article
                has_neurodegenerative = False
                has_smell_disorder = False

                # Check for entities in the subsequent lines
                continue

            # Handle annotations (tab or space-separated)
            parts = line.split()  # Split by whitespace (space or tab)

            # Check if this is an entity line
            if len(parts) >= 6:  # Expecting at least 6 parts
                entity_id = parts[5].strip()  # Get the entity ID from position 5
                if entity_id in neurodegenerative_ids:
                    total_neurodegenerative_entities += 1
                    has_neurodegenerative = True
                elif entity_id == smell_disorder_id:
                    total_smell_disorder_entities += 1
                    has_smell_disorder = True

            # Handle relations between neurodegenerative diseases and smell disorders
            elif len(parts) >= 4:  # Expecting at least PMID, relation type, entity, ...
                pmid_relation = parts[0].strip()
                relation_type = parts[1].strip()
                entity_id = parts[2].strip()

                if pmid_relation in pmids:  # Only consider if this PMID has been seen
                    if entity_id in neurodegenerative_ids or entity_id == smell_disorder_id:
                        relations.append((pmid_relation, relation_type, entity_id))
                        relation_counts[relation_type] += 1  # Count relations by type

        # After processing the lines, check the flags
        if has_neurodegenerative:
            neurodegenerative_pmids.add(pmid)
        if has_smell_disorder:
            smell_disorder_pmids.add(pmid)
        if has_neurodegenerative and has_smell_disorder:
            both_pmids.add(pmid)
            both_entities_articles.append(article)  # Add the entire article to the list

    # Prepare the final data summary
    summary = {
        'Total Articles': len(pmids),
        'Articles with Neurodegenerative Diseases': len(neurodegenerative_pmids),
        'Articles with Smell Disorder': len(smell_disorder_pmids),
        'Articles with Both Neurodegenerative and Smell Disorder': len(both_pmids),
        'Relations between Neurodegenerative Diseases and Smell Disorders': len(relations),
        'Total Neurodegenerative Entities': total_neurodegenerative_entities,
        'Total Smell Disorder Entities': total_smell_disorder_entities,
        'Relations Details': relations,  # Optional: show details if needed
        'Relation Counts': relation_counts,  # Relation counts by type
        'Both Entities Articles': both_entities_articles  # Store articles containing both entities
    }

    # Write the subset of articles containing both entities to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for article in both_entities_articles:
            output_file.write(article + '\n\n')  # Write each article with double newline

    return summary

# Example usage
file_path = 'neurodegenerative-disease/SessionNumber.txt'  # Update with the actual file path
output_file_path = 'neurodegenerative-disease/output_subset.txt'  # Update with the desired output file path
summary_data = parse_pubtator_file(file_path, output_file_path)

# Print only the counts
print(f"Total Articles: {summary_data['Total Articles']}")
print(f"Articles with Neurodegenerative Diseases: {summary_data['Articles with Neurodegenerative Diseases']}")
print(f"Articles with Smell Disorder: {summary_data['Articles with Smell Disorder']}")
print(
    f"Articles with Both Neurodegenerative and Smell Disorder: {summary_data['Articles with Both Neurodegenerative and Smell Disorder']}")
print(
    f"Relations between Neurodegenerative Diseases and Smell Disorders: {summary_data['Relations between Neurodegenerative Diseases and Smell Disorders']}")
print(f"Total Neurodegenerative Entities: {summary_data['Total Neurodegenerative Entities']}")
print(f"Total Smell Disorder Entities: {summary_data['Total Smell Disorder Entities']}")

# Print relation counts by type
print("\nRelation Counts by Type:")
for relation_type, count in summary_data['Relation Counts'].items():
    print(f"{relation_type}: {count}")





