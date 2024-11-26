import spacy
import random
from collections import defaultdict

# Load a SpaCy model
nlp = spacy.load("en_core_web_sm")


def parse_pubtator_file(file_path, output_file_path, sample_size=500):
    data = {}

    # Read the contents of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        pubtator_text = file.read()

    # Split the input into articles for processing (separated by double newlines)
    articles = pubtator_text.strip().split('\n\n')

    # Initialize counters and structures for the summary
    pmids = set()  # To store unique PMIDs
    neurodegenerative_pmids = set()
    smell_disorder_pmids = set()
    both_pmids = set()
    relations = []
    relation_counts = defaultdict(int)

    # Define the MESH IDs for neurodegenerative and smell disorder terms
    neurodegenerative_ids = {
        'MESH:D000544', 'MESH:C537240', 'MESH:D003704', 'MESH:D019636', 'MESH:D010300'
    }
    smell_disorder_id = 'MESH:D000857'
    species_id = '9606'  # Species ID for humans

    # Initialize counters for totals
    total_neurodegenerative_entities = 0
    total_smell_disorder_entities = 0
    total_species_entities = 0  # New counter for Species 9606 as perceivers

    # Randomly select a sample of articles
    selected_articles = random.sample(articles, sample_size)
    selected_pmids = set()  # Track PMIDs of selected articles
    both_entities_articles = []

    # Iterate through the selected articles
    for article in selected_articles:
        lines = article.strip().split('\n')
        current_pmid = None
        has_neurodegenerative = False
        has_smell_disorder = False
        has_species = False

        for line in lines:
            # Process abstract and PMID
            if '|a|' in line:
                pmid, _, abstract = line.partition('|a|')
                pmid = pmid.strip()
                pmids.add(pmid)
                selected_pmids.add(pmid)
                current_pmid = pmid
                continue

            # Process each entity or relation in the article
            parts = line.split()
            if len(parts) >= 6:
                entity_id = parts[5].strip()

                # Count neurodegenerative and smell disorder terms by MESH ID
                if entity_id in neurodegenerative_ids:
                    total_neurodegenerative_entities += 1
                    has_neurodegenerative = True
                elif entity_id == smell_disorder_id:
                    total_smell_disorder_entities += 1
                    has_smell_disorder = True
                elif entity_id == species_id:  # Count Species 9606 as perceivers
                    total_species_entities += 1
                    has_species = True

            # Track relations if related to selected IDs
            elif len(parts) >= 4:
                pmid_relation = parts[0].strip()
                relation_type = parts[1].strip()
                entity_id = parts[2].strip()
                if pmid_relation in selected_pmids:
                    if entity_id in neurodegenerative_ids or entity_id == smell_disorder_id:
                        relations.append((pmid_relation, relation_type, entity_id))
                        relation_counts[relation_type] += 1

        # Track articles containing each type of entity
        if has_neurodegenerative:
            neurodegenerative_pmids.add(current_pmid)
        if has_smell_disorder:
            smell_disorder_pmids.add(current_pmid)
        if has_neurodegenerative and has_smell_disorder:
            both_pmids.add(current_pmid)
            both_entities_articles.append(article)

    # Prepare the final data summary
    summary = {
        'Total Articles': len(selected_pmids),
        'Articles with Neurodegenerative Diseases': len(neurodegenerative_pmids),
        'Articles with Smell Disorder': len(smell_disorder_pmids),
        'Articles with Both Neurodegenerative and Smell Disorder': len(both_pmids),
        'Relations between Neurodegenerative Diseases and Smell Disorders': len(relations),
        'Total Neurodegenerative Entities': total_neurodegenerative_entities,
        'Total Smell Disorder Entities': total_smell_disorder_entities,
        'Total Perceiver Entities (Species 9606)': total_species_entities,
        'Relations Details': relations,
        'Relation Counts': relation_counts,
        'Both Entities Articles': both_entities_articles
    }

    # Write the subset of articles to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for article in both_entities_articles:
            output_file.write(article + '\n\n')

    return summary


# Example usage
file_path = 'SessionNumber.txt'
output_file_path = 'output_subset_500.txt'
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
print(f"Total Perceiver Entities (Species 9606): {summary_data['Total Perceiver Entities (Species 9606)']}")

# Print relation counts by type
print("\nRelation Counts by Type:")
for relation_type, count in summary_data['Relation Counts'].items():
    print(f"{relation_type}: {count}")
