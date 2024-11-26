import re
import random
from sklearn.model_selection import train_test_split
import nltk
from nltk.tokenize import sent_tokenize

# Ensure you download the required NLTK resources
nltk.download('punkt')

# Define sets of terms for each entity type, using regular expressions for variations
neurodegenerative_terms = {
    r'\balzheimer[s]?\s+disease\b',  # "alzheimer disease" or "alzheimer's disease"
    r'\bad\b', r'\bparkinson[s]?\s+disease\b',
    r'\bneurodegenerative\s+disease\b', r'\bnd\b', r'\bms\b',
    r'\bmultiple\s+sclerosis\b', r'\bdementia\b'
}
olfactory_terms = {
    r'\bsmell\s+loss\b', r'\bhyposmia\b', r'\banosmia\b', r'\bsmell\s+disorder\b',
    r'\bsmell\s+dysfunction\b', r'\baltered\s+sense\s+of\s+smell\b', r'\bparosmia\b', r'\bphantosmia\b'
}
smell_test_terms = {
    r'\bupsit\b', r'\bbsit\b', r'\bscentinel\b', r"\bsniffin'\s+sticks\b", r'\bnih\s+toolbox\b', r'\bsmell\s+test\b',
    r'\bolfactory\s+evaluation\b', r'\bsmell\s+function\s+test\b', r'\bsmell\s+identification\s+test\b',
    r'\bolfactory\s+threshold\s+test\b', r'\bolfactory\s+identification\s+test\b', r'\bolfactory\s+dysfunction\s+test\b'
}
smell_source_terms = {
    r'\bodorant\b', r'\bvolatile\b', r'\bvanillin\b', r'\bphenyl\s+ethyl\s+alcohol\b',
    r'\bpea\b', r'\bn-butanol\b', r'\blimonene\b', r'\beucalyptol\b', r'\bcarvone\b',
    r'\bisoamylacetate\b', r'\bacetaldehyde\b', r'\bcinnamon\s+aldehyde\b',
    r'\bessential\s+oil\b', r'\bpeppermint\b', r'\borange\b', r'\bclove\b'
}
perceiver_terms = {
    r'\bparticipants\b', r'\bhuman\s+subjects\b', r'\bmale\b', r'\bfemale\b',
    r'\bhuman\b', r'\bsubjects\b', r'\bwomen\b', r'\bmen\b', r'\bpatients\b', r'\bpatient\b'
}

def tag_entities(text):
    """Tag entities in the given text using the BIO format, including I- tags for multi-word entities."""
    tags = []
    words = text.split()

    # Initialize a set to keep track of current entity tags
    current_entity = None

    # Tagging function for each entity type
    for word in words:
        lower_word = word.lower()
        found_tag = False

        for term in neurodegenerative_terms:
            if re.fullmatch(term, lower_word):
                if current_entity == 'B-NEURODEGENERATIVE':
                    tags.append((word, 'I-NEURODEGENERATIVE'))
                else:
                    tags.append((word, 'B-NEURODEGENERATIVE'))
                    current_entity = 'B-NEURODEGENERATIVE'
                found_tag = True
                break
        if not found_tag:
            for term in olfactory_terms:
                if re.fullmatch(term, lower_word):
                    if current_entity == 'B-OLFACTORY':
                        tags.append((word, 'I-OLFACTORY'))
                    else:
                        tags.append((word, 'B-OLFACTORY'))
                        current_entity = 'B-OLFACTORY'
                    found_tag = True
                    break
        if not found_tag:
            for term in smell_test_terms:
                if re.fullmatch(term, lower_word):
                    if current_entity == 'B-SMELL_TEST':
                        tags.append((word, 'I-SMELL_TEST'))
                    else:
                        tags.append((word, 'B-SMELL_TEST'))
                        current_entity = 'B-SMELL_TEST'
                    found_tag = True
                    break
        if not found_tag:
            for term in smell_source_terms:
                if re.fullmatch(term, lower_word):
                    if current_entity == 'B-SMELL_SOURCE':
                        tags.append((word, 'I-SMELL_SOURCE'))
                    else:
                        tags.append((word, 'B-SMELL_SOURCE'))
                        current_entity = 'B-SMELL_SOURCE'
                    found_tag = True
                    break
        if not found_tag:
            for term in perceiver_terms:
                if re.fullmatch(term, lower_word):
                    if current_entity == 'B-PERCIEVER':
                        tags.append((word, 'I-PERCIEVER'))
                    else:
                        tags.append((word, 'B-PERCIEVER'))
                        current_entity = 'B-PERCIEVER'
                    found_tag = True
                    break

        if not found_tag:
            tags.append((word, 'O'))  # Outside any entity
            current_entity = None  # Reset current entity

    return tags


def process_article_file(input_file_path, output_tags_path, train_file_path, test_file_path, test_size=0.2):
    """Process the article file to extract and tag entities, and split into train/test sets."""
    all_tags = []

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
                    title = line.split('|t|')[1].strip()
                elif '|a|' in line:
                    abstract = line.split('|a|')[1].strip()

            # Combine title and abstract for analysis
            text = f"{title} {abstract}"

            # Split text into sentences using NLTK
            sentences = sent_tokenize(text)

            # Tag entities in each sentence
            for sentence in sentences:
                # Lowercase and remove punctuation for each sentence before tagging
                cleaned_sentence = re.sub(r'[^\w\s]', '', sentence).lower()
                tags = tag_entities(cleaned_sentence)
                all_tags.append(tags)

    # Write train tags to train output file with blank lines separating sentences
    with open(train_file_path, 'w', encoding='utf-8') as train_file:
        for tags in all_tags:
            for word, tag in tags:
                train_file.write(f"{word}\t{tag}\n")
            train_file.write("\n")  # Add a blank line to separate sentences

    # Write test tags to test output file with blank lines separating sentences
    with open(test_file_path, 'w', encoding='utf-8') as test_file:
        for tags in all_tags:
            for word, tag in tags:
                test_file.write(f"{word}\t{tag}\n")
            test_file.write("\n")  # Add a blank line to separate sentences

    # Write all tags to the main output file with blank lines separating sentences
    with open(output_tags_path, 'w', encoding='utf-8') as output_file:
        for tags in all_tags:
            for word, tag in tags:
                output_file.write(f"{word}\t{tag}\n")
            output_file.write("\n")  # Add a blank line to separate sentences

    # Debug print to verify functionality
    print("Entities tagged, train/test sets created, and results saved to output files.")


# Example usage
input_file_path = 'output_subset.txt'  # Path to your subset file
output_tags_path = 'entity_tags.txt'  # Output path for all tags
train_file_path = 'train_tags.txt'  # Output path for training tags
test_file_path = 'test_tags.txt'  # Output path for testing tags
process_article_file(input_file_path, output_tags_path, train_file_path, test_file_path)
