import requests
from xml.etree import ElementTree
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def search_pubmed(query, max_results=100):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    search_url = f"{base_url}esearch.fcgi"
    fetch_url = f"{base_url}efetch.fcgi"
    
    # Step 1: Search for articles
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "xml"
    }
    search_response = requests.get(search_url, params=search_params)
    search_tree = ElementTree.fromstring(search_response.content)
    id_list = [id_elem.text for id_elem in search_tree.findall(".//Id")]
    
    # Step 2: Fetch details for each article
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "retmode": "xml"
    }
    fetch_response = requests.get(fetch_url, params=fetch_params)
    fetch_tree = ElementTree.fromstring(fetch_response.content)
    
    # Step 3: Parse results
    articles = []
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
        
        articles.append({
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "pub_year": pub_year
        })
    
    return articles

# Fetch data
query = "rabies"
articles = search_pubmed(query, max_results=100)

# Process data for visualization
pub_years = [article['pub_year'] for article in articles if article['pub_year'] != "Unknown"]
pub_years_df = pd.DataFrame(pub_years, columns=["Year"])

# Visualization
plt.figure(figsize=(10, 6))
sns.countplot(y="Year", data=pub_years_df, order=pub_years_df['Year'].value_counts().index)
plt.title("Number of PubMed Articles on Rabies per Year")
plt.xlabel("Number of Articles")
plt.ylabel("Year")
plt.show()