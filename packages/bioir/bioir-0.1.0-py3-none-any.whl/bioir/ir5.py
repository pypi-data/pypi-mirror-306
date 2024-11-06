print("""import requests
from bs4 import BeautifulSoup

# Base URL of the e-commerce site with pagination structure
base_url = 'http://books.toscrape.com/catalogue/page-{}.html'

# Function to scrape product data from a single page
def scrape_books(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure the request was successful
    soup = BeautifulSoup(response.content, 'html.parser')
    
    books = []
    for product in soup.select('article.product_pod'):
        title = product.h3.a['title']
        price = product.select_one('.price_color').get_text(strip=True)
        link = product.h3.a['href']
        full_link = requests.compat.urljoin(url, link)  # Join relative link with base URL

        books.append({
            'title': title,
            'price': price,
            'link': full_link
        })
    return books

# Loop through multiple pages
all_books = []
for page_num in range(1, 6):  # Adjust the range based on the number of pages
    url = base_url.format(page_num)
    try:
        books_data = scrape_books(url)
        if not books_data:  # Stop if no books are found on the page (end of pagination)
            break
        all_books.extend(books_data)
        print(f"Page {page_num} scraped successfully.")
    except requests.HTTPError as e:
        print(f"Failed to scrape page {page_num}: {e}")
        break

# Print all book data collected
for book in all_books:
    print(f"Title: {book['title']}")
    print(f"Price: {book['price']}")
    print(f"Link: {book['link']}")
    print('-' * 40)""")
