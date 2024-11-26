import requests

# Function to fetch title and abstract using PubMed eUtils API
def fetch_pubmed_data(pmid):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=json"
    response = requests.get(url)
    if response.status_code == 200:
        summary_data = response.json()
        title = summary_data['result'][str(pmid)]['title']
        abstract = summary_data['result'][str(pmid)].get('abstract', 'No abstract available')
        return title, abstract
    else:
        return None, None

# Loop through PMIDs and fetch title and abstract
for pmid in pmids:
    title, abstract = fetch_pubmed_data(pmid)
    print(f"PMID: {pmid}")
    print(f"Title: {title}")
    print(f"Abstract: {abstract}")
    print("\n")
