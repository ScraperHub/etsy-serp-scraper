# etsy-product-listing-scraper

## Description

This repository contains a Python scraper for extracting product listings from Etsy's search pages. It uses the [Crawlbase Crawling API](https://crawlbase.com/crawling-api-avoid-captchas-blocks) to bypass blocks and handle JavaScript rendering. The scraper collects product titles, prices, and ratings and stores them in CSV or SQLite for easy analysis.

➡ Read the full blog [here](https://crawlbase.com/blog/scrape-etsy-product-listing/) to learn more.

## Scraper Overview

### Etsy Product Listing Scraper

The `etsy_product_listing_scraper.py` extracts:

1. **Product Title**
2. **Price**
3. **Rating**

The scraper also handles pagination to collect data from multiple search result pages and supports two output formats:

- **CSV file** (`etsy_product_data.csv`)
- **SQLite database** (`etsy_products.db`)

## Environment Setup

Ensure Python 3.7 or higher is installed. Check the version using:

```bash
python --version
```

Install the required dependencies:

```bash
pip install crawlbase beautifulsoup4 pandas
```

- **Crawlbase** – Handles dynamic rendering and bot protection.
- **BeautifulSoup** – Parses and extracts HTML elements.
- **pandas** – Saves data to CSV.
- **sqlite3** – (Built-in) Saves data to a local database.

## Running the Scraper

1. **Get Your Crawlbase Access Token**

   - Sign up at [Crawlbase](https://crawlbase.com/signup) to get your API token.

2. **Update the Scraper**
   - Replace `"YOUR_CRAWLBASE_JS_TOKEN"` in `etsy_product_listing_scraper.py` with your token.

Run the Scraper

```bash
python etsy_product_listing_scraper.py
```

The scraper will fetch data from all pages for a given query (default is `clothes`) and save the results to your selected output format.

## To-Do List

- Add support for dynamic query inputs via CLI.
- Export results in JSON format.
- Enhance selector logic for more robust scraping.
- Add retry logic for large-scale runs.

This scraper is ideal for ecommerce researchers, market analysts, and developers building Etsy data pipelines. 🛒
