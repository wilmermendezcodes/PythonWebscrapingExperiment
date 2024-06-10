import requests
from xml.etree import ElementTree
import time
import csv

def search_pubmed(query, max_results=1000):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    search_url = f"{base_url}esearch.fcgi"
    fetch_url = f"{base_url}efetch.fcgi"
    
    headers = {
        "User-Agent": "RabiesResearch/1.0 (WilmerMendez500@outlook.com)"
    }
    
    # Step 1: Get the total number of results
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": 0,  # We only want the count here
        "retmode": "xml"
    }
    search_response = requests.get(search_url, params=search_params, headers=headers)
    search_tree = ElementTree.fromstring(search_response.content)
    total_count = int(search_tree.find(".//Count").text)
    print(f"Total articles found: {total_count}")
    
    all_articles = []
    batch_size = 100  # Fetch results in batches of 100 to avoid overloading the server
    
    for start in range(0, total_count, batch_size):
        # Step 2: Search for articles in batches
        search_params.update({
            "retstart": start,
            "retmax": batch_size
        })
        search_response = requests.get(search_url, params=search_params, headers=headers)
        search_tree = ElementTree.fromstring(search_response.content)
        id_list = [id_elem.text for id_elem in search_tree.findall(".//Id")]
        
        # Step 3: Fetch details for each batch of articles
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "xml"
        }
        fetch_response = requests.get(fetch_url, params=fetch_params, headers=headers)
        fetch_tree = ElementTree.fromstring(fetch_response.content)
        
        for article in fetch_tree.findall(".//PubmedArticle"):
            title_elem = article.find(".//ArticleTitle")
            title = title_elem.text if title_elem is not None else "No title available"
            
            abstract_elem = article.find(".//Abstract/AbstractText")
            abstract = abstract_elem.text if abstract_elem is not None else "No abstract available"
            
            authors = []
            for author in article.findall(".//Author"):
                last_name = author.find("LastName").text if author.find("LastName") is not None else ""
                fore_name = author.find("ForeName").text if author.find("ForeName") is not None else ""
                authors.append(f"{last_name} {fore_name}".strip())
            
            pub_date_elem = article.find(".//PubDate/Year")
            pub_year = pub_date_elem.text if pub_date_elem is not None else "Unknown"
            
            all_articles.append({
                "title": title,
                "abstract": abstract,
                "authors": ", ".join(authors),
                "pub_year": pub_year
            })
        
        print(f"Fetched articles {start + 1} to {start + batch_size} of {total_count}")
        time.sleep(1)  # To respect API rate limits
    
    return all_articles

def save_to_csv(articles, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["title", "abstract", "authors", "pub_year"])
        writer.writeheader()
        for article in articles:
            writer.writerow(article)

# Fetch all articles related to rabies
query = "rabies"
articles = search_pubmed(query)

# Save the data to a CSV file
csv_filename = "pubmed_rabies_articles.csv"
save_to_csv(articles, csv_filename)
print(f"Data saved to {csv_filename}")