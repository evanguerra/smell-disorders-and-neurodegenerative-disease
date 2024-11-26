import sys


def convert_newline_to_comma(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        # Read all PMIDs, strip any whitespace, and filter out empty lines
        pmids = [line.strip() for line in infile if line.strip()]

    # Join PMIDs with a comma
    pmid_string = ",".join(pmids)

    # Write the result to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(pmid_string)

    print(f"PMIDs converted and saved to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_pmids.py [input_file] [output_file]")
        print("\t[input_file]: The input file with newline-separated PMIDs")
        print("\t[output_file]: The output file with comma-separated PMIDs")
        print("Example: python convert_pmids.py pmid_list.txt pmid_comma_separated.txt")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        convert_newline_to_comma(input_file, output_file)
