import re
from collections import defaultdict

# Define sets of terms for each entity type, using regular expressions for variations
neurodegenerative_terms = {
    r'\balzheimer\b', r'\bad\b', r'\bparkinson\b', r'\bparkinsonian\b',
    r'\bneurodegenerative disease\b', r'\bnd\b', r'\bms\b',
    r'\bmultiple sclerosis\b', r'\bdementia\b', r'\balzheimers\b', r'\bparkinsons\b', r'\bparkinsons disease\b',
    r'\balzheimers disease\b', r'\bpd\b'
}
olfactory_terms = {
    r'\bsmell loss\b', r'\bhyposmia\b', r'\banosmia\b', r'\bsmell disorder\b',
    r'\bsmell dysfunction\b', r'\baltered sense of smell\b', r'\bparosmia\b', r'\bphantosmia\b'
}
smell_test_terms = {
    r'\bupsit\b', r'\bbsit\b', r'\bscentinel\b', r"\bsniffin' sticks\b", r'\bnih toolbox\b', r'\bsmell test\b',
    r'\bolfactory evaluation\b', r'\bsmell function test\b', r'\bsmell indentification test\b',
    r'\bolfactory threshhold test\b', r'\bolfactory identification test\b', r'\bolfactory dysfunction test\b'
}
smell_source_terms = {
    r'\bodorant\b', r'\bvolatile\b', r'\bvanillin\b', r'\bphenyl ethyl alcohol\b',
    r'\bpea\b', r'\bn-butanol\b', r'\blimonene\b', r'\beucalyptol\b', r'\bcarvone\b',
    r'\bisoamylacetate\b', r'\bacetaldehyde\b', r'\bcinnamon aldehyde\b',
    r'\bessential oil\b', r'\bpeppermint\b', r'\borange\b', r'\bclove\b',
    r'\bupsit\b', r'\bbsit\b', r'\bscentinel\b', r"\bsniffin' sticks\b", r'\bnih toolbox\b', r'\bsmell test\b',
    r'\bolfactory evaluation\b', r'\bsmell function test\b', r'\bsmell indentification test\b',
    r'\bolfactory threshhold test\b', r'\bolfactory identification test\b', r'\bolfactory dysfunction test\b'
}
perceiver_terms = {
    r'\bparticipants\b', r'\bhuman subjects\b', r'\bmale\b', r'\bfemale\b',
    r'\bhuman\b', r'\bsubjects\b', r'\bwomen\b', r'\bmen\b', r'\bpatients\b', r'\bpatient\b'
}


def process_article_file(input_file_path, output_counts_path):
    # Initialize counters for each entity type
    neurodegenerative_counts = defaultdict(int)
    olfactory_counts = defaultdict(int)
    smell_test_counts = defaultdict(int)
    smell_source_counts = defaultdict(int)
    perceiver_counts = defaultdict(int)

    with open(input_file_path, 'r', encoding='utf-8') as file:
        # Split file into individual articles
        articles = file.read().strip().split('\n\n')

        for article in articles:
            # Initialize variables for the title and abstract
            title = ''
            abstract = ''

            # Process each line in the article
            for line in article.splitlines():
                if '|t|' in line:
                    title = line.split('|t|')[1].strip().lower()
                elif '|a|' in line:
                    abstract = line.split('|a|')[1].strip().lower()

            # Combine title and abstract for analysis
            text = f"{title} {abstract}"

            # Strip punctuation using regex
            text = re.sub(r'[^\w\s]', '', text)

            # Count terms for each entity type
            for term in neurodegenerative_terms:
                neurodegenerative_counts[term] += len(re.findall(term, text))

            for term in olfactory_terms:
                olfactory_counts[term] += len(re.findall(term, text))

            for term in smell_test_terms:
                smell_test_counts[term] += len(re.findall(term, text))

            for term in smell_source_terms:
                smell_source_counts[term] += len(re.findall(term, text))

            for term in perceiver_terms:
                perceiver_counts[term] += len(re.findall(term, text))

    # Calculate total counts for each entity type
    total_neurodegenerative = sum(neurodegenerative_counts.values())
    total_olfactory = sum(olfactory_counts.values())
    total_smell_test = sum(smell_test_counts.values())
    total_smell_source = sum(smell_source_counts.values())
    total_perceiver = sum(perceiver_counts.values())

    # Write counts to output file
    with open(output_counts_path, 'w', encoding='utf-8') as output_file:
        output_file.write("Neurodegenerative Disease Entity Counts:\n")
        for term, count in sorted(neurodegenerative_counts.items(), key=lambda x: x[1], reverse=True):
            output_file.write(f"{term}: {count}\n")
        output_file.write(f"Total neurodegenerative count: {total_neurodegenerative}\n")

        output_file.write("\nOlfactory Entity Counts:\n")
        for term, count in sorted(olfactory_counts.items(), key=lambda x: x[1], reverse=True):
            output_file.write(f"{term}: {count}\n")
        output_file.write(f"Total olfactory count: {total_olfactory}\n")

        output_file.write("\nSmell Test Entity Counts:\n")
        for term, count in sorted(smell_test_counts.items(), key=lambda x: x[1], reverse=True):
            output_file.write(f"{term}: {count}\n")
        output_file.write(f"Total smell test count: {total_smell_test}\n")

        output_file.write("\nSmell Source Entity Counts:\n")
        for term, count in sorted(smell_source_counts.items(), key=lambda x: x[1], reverse=True):
            output_file.write(f"{term}: {count}\n")
        output_file.write(f"Total smell source count: {total_smell_source}\n")

        output_file.write("\nPerceiver Entity Counts:\n")
        for term, count in sorted(perceiver_counts.items(), key=lambda x: x[1], reverse=True):
            output_file.write(f"{term}: {count}\n")
        output_file.write(f"Total perceiver count: {total_perceiver}\n")

    # Debug print to verify functionality
    print("Counts calculated, totals computed, and results saved to output.")

# Example usage
input_file_path = 'output_subset.txt'  # Path to your subset file
output_counts_path = 'entity_counts.txt'  # Output path for counts
process_article_file(input_file_path, output_counts_path)
