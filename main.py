import requests
from bs4 import BeautifulSoup
import csv
import time

# Function to extract product details from the product page
def extract_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_name = soup.find('span', {'class': 'a-size-large product-title-word-break'}).text.strip()
    product_price = soup.find('span', {'class': 'a-price-whole'}).text.strip()
    try:
        rating = soup.find('span', {'class': 'a-icon-alt'}).text.strip()
    except:
        rating = ''
    try:
        num_reviews = soup.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text.strip()
    except:
        num_reviews = ''
    try:
        description = soup.find('div', {'id': 'productDescription'}).text.strip()
    except:
        description = ''
    try:
        asin = soup.find('div', {'data-asin': True})['data-asin']
    except:
        asin = ''
    try:
        manufacturer = soup.find('a', {'id': 'bylineInfo'}).text.strip()
    except:
        manufacturer = ''
    return product_name, product_price, rating, num_reviews, description, asin, manufacturer

# Main function to extract product information from the search result pages
def extract_data(url, page):
    response = requests.get(url.format(page))
    soup = BeautifulSoup(response.text, 'html.parser')
    all_products = soup.find_all('div', {'data-component-type': 's-search-result'})
    data = []
    for product in all_products:
        try:
            product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal s-no-outline'})['href']
            product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
            product_price = product.find('span', {'class': 'a-price-whole'}).text.strip()
            try:
                rating = product.find('span', {'class': 'a-icon-alt'}).text.strip()
            except:
                rating = ''
            try:
                num_reviews = product.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text.strip()
            except:
                num_reviews = ''
            product_details = extract_product_details(product_url)
            data.append([product_url, product_name, product_price, rating, num_reviews] + list(product_details))
            print('Product scraped: ', product_name)
        except:
            print('Error scraping product')
    return data

# URLs to scrape
url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'
pages = 20

# Extracting data from search result pages
all_data = []
for page in range(1, pages+1):
    print('Scraping page: ', page)
    data = extract_data(url, page)
    all_data.extend(data)
    time.sleep(5)

# Saving data to CSV file
with open('amazon_products.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Manufacturer'])
    writer