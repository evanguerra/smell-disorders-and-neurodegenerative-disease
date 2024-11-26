import requests
import os
import sys
import time
from unidecode import unidecode


def submit_pmids_request(input_file, bioconcept, output_file_session_number):
    unicode_to_regular = {}

    # Load the unicode translation table
    with open('neurodegenerative-disease/lib/unicode.txt', 'r', encoding='utf-8') as input_file_unicode:
        for line in input_file_unicode:
            line = line.strip()
            parts = line.split("\t")
            if len(parts) == 2:
                uni, reg = parts
                unicode_to_regular[uni] = reg

    with open(output_file_session_number, 'w', encoding='utf-8') as output_file:
        with open(input_file, 'r', encoding='utf-8') as pmid_file:
            pmids = []
            for line in pmid_file:
                pmid = line.strip()
                if pmid:  # Skip empty lines
                    pmids.append(pmid)

            # Process PMIDs in batches of 100
            for i in range(0, len(pmids), 100):
                batch_pmids = pmids[i:i + 100]
                pmids_string = ','.join(batch_pmids)

                # Prepare and send the request to PubTator using the PMIDs
                url = f"https://www.ncbi.nlm.nih.gov/research/pubtator3-api/publications/export/pubtator?pmids={pmids_string}"
                print(f"Submitting PMIDs: {pmids_string}")

                try:
                    # Send the request
                    response = requests.get(url)

                    # Debugging: Log the response status code
                    print(f"Response status code: {response.status_code}")

                    if response.status_code == 200:
                        # Successfully retrieved data
                        annotations = response.text
                        output_file.write(f"PMIDs: {pmids_string}\n")
                        output_file.write("Annotations:\n")
                        output_file.write(annotations + "\n\n")
                        output_file.flush()  # Ensure immediate writing to file
                    else:
                        print(f"Error: HTTP {response.status_code} for PMIDs: {pmids_string}")

                except Exception as e:
                    print(f"Exception occurred for PMIDs: {pmids_string}: {str(e)}")

                # Respect the 3 seconds delay
                time.sleep(3)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python submit_pmids_request.py [Inputfile] [Bioconcept] [outputfile_SessionNumber]")
        print("\t[Inputfile]: a file containing a list of PMIDs separated by newlines")
        print("\t[Bioconcept]: Gene, Disease, Chemical, Species, Mutation, and All.")
        print("\t[outputfile_SessionNumber]: output file to save session numbers and annotations.")
        print("Example: python submit_pmids_request.py pmid_list.txt All SessionNumber.txt")
    else:
        input_file = sys.argv[1]
        bioconcept = sys.argv[2]
        output_file_session_number = sys.argv[3]
        submit_pmids_request(input_file, bioconcept, output_file_session_number)
