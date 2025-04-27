import pandas as pd
import sqlite3
from bs4 import BeautifulSoup
from crawlbase import CrawlingAPI

# Initialize the CrawlingAPI class with your Crawlbase API token
api = CrawlingAPI({'token': 'YOUR_CRAWLBASE_JS_TOKEN'})

# options for Crawling API
options = {
 'page_wait': 5000,
 'ajax_wait': 'true'
}

def create_database():
    conn = sqlite3.connect('etsy_products.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT,
                      price TEXT,
                      rating TEXT
                    )''')
    conn.commit()
    conn.close()

def save_to_database(data):
    conn = sqlite3.connect('etsy_products.db')
    cursor = conn.cursor()

    # Create a list of tuples from the data
    data_tuples = [(product['title'], product['price'], product['rating']) for product in data]

    # Insert data into the products table
    cursor.executemany('''
        INSERT INTO products (title, price, rating)
        VALUES (?, ?, ?)
    ''', data_tuples)

    conn.commit()
    conn.close()

def get_total_pages(search_url):
    try:
        response = api.get(search_url, options)
        if response['status_code'] == 200:
            search_page_html = response['body'].decode('latin1')
            soup = BeautifulSoup(search_page_html, 'html.parser')
            total_pages = int(soup.select_one('div[data-appears-component-name="search_pagination"] nav ul.search-pagination li:nth-last-child(3) a').text)
            return total_pages
    except Exception as e:
        print(f"An error occurred while fetching total pages: {e}")
    return 1

def scrape_page(page_url):
    try:
        response = api.get(page_url, options)
        if response['status_code'] == 200:
            page_html = response['body'].decode('latin1')
            page_soup = BeautifulSoup(page_html, 'html.parser')
            product_containers = page_soup.select('div.search-listings-group div[data-search-results-container] ol li')
            product_details = []
            for container in product_containers:
                product = {}
                # Extract product name
                titleElement = container.select_one('div.v2-listing-card__info h3.v2-listing-card__title')
                product['title'] = titleElement.text.strip() if titleElement else ''
                # Extract product price
                priceElement = container.select_one('div.n-listing-card__price p.lc-price span.currency-value')
                product['price'] = priceElement.text.strip() if priceElement else ''
                # Extract product rating
                ratingElement = container.select_one('div.v2-listing-card__info div.shop-name-with-rating span.larger_review_stars > div')
                product['rating'] = ratingElement.text.strip() if ratingElement else ''
                product_details.append(product)
            return product_details
    except Exception as e:
        print(f"An error occurred while scraping page: {e}")
    return []

def main():
    # Define the search query
    search_query = 'clothes'

    # Construct the request URL for the first page
    search_url = f'https://www.etsy.com/search?q={search_query}'

    total_pages = get_total_pages(search_url)
    all_product_details = []

    for page in range(1, total_pages + 1):
        page_url = f'{search_url}&page={page}'
        page_product_details = scrape_page(page_url)
        all_product_details.extend(page_product_details)

    # Save scraped data as a CSV file
    df = pd.DataFrame(all_product_details)
    df.to_csv('etsy_product_data.csv', index=False)

    # Insert scraped data into the SQLite database
    save_to_database(all_product_details)

if __name__ == "__main__":
    main()