print("""import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import matplotlib.pyplot as plt

def get_links(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'html.parser')
        return {urljoin(url, a['href']) for a in soup.find_all('a', href=True) 
                if urljoin(url, a['href']).startswith(url)}
    except:
        return set()

# Websites to analyze
websites = [
    'https://www.ted.com',
    'https://www.goodreads.com',
    'https://www.airbnb.com',
    'https://www.khanacademy.org'
]

# Get links for each website
link_map = {url: get_links(url) for url in websites}

# Calculate PageRank
d = 0.85  # damping factor
pagerank = {url: 1/len(websites) for url in websites}

# Run PageRank algorithm for 20 iterations
for _ in range(20):
    new_rank = {}
    for page in websites:
        # Calculate incoming PageRank
        incoming_pr = sum(pagerank[src] / len(links) 
                         for src, links in link_map.items() 
                         if page in links and links)
        # Update PageRank
        new_rank[page] = (1 - d) / len(websites) + d * incoming_pr
    pagerank = new_rank

# Normalize scores
total = sum(pagerank.values())
pagerank = {url: score/total for url, score in pagerank.items()}

# Plot results
plt.figure(figsize=(10, 5))
sorted_pr = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
sites, scores = zip(*sorted_pr)
plt.barh([site.replace('https://www.', '').replace('.com', '').replace('.org', '') 
          for site in sites], scores)
plt.xlabel('PageRank Score')
plt.title('Website PageRank Scores')
plt.tight_layout()
plt.show()

# Print scores
for url, score in sorted_pr:
    print(f'{url}: {score:.6f}')""")