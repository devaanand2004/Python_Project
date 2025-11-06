import requests
from bs4 import BeautifulSoup
import random
import logging
import streamlit as st
from PIL import Image
import time

logging.basicConfig(
    filename='price_tracker.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                      "Version/14.0 Safari/605.1.15",
        "Accept-Language": "en-US,en;q=0.9"
    },
]

amazon_logo = Image.open(
    r"C:\Users\Asus\OneDrive\Documents\Pictures\Screenshots\Screenshot 2024-10-07 233948.png")
flipkart_logo = Image.open(r"C:\Users\Asus\OneDrive\Documents\flipkart_logo.png")


def get_page(url):
    headers = random.choice(HEADERS_LIST)
    max_retries = 3
    retry_delay = 2
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred for {url}: {http_err}")
        except requests.exceptions.Timeout:
            logging.error(f"Request timed out for {url}. Retrying...")
        except requests.exceptions.RequestException as err:
            logging.error(f"Request error for {url}: {err}")

        time.sleep(retry_delay)

    return None


def parse_price(html_content, site_name):
    soup = BeautifulSoup(html_content, 'lxml')

    price = None
    if site_name == 'Amazon':
        # Look for various price elements
        price_elements = soup.find_all('span', class_='a-price-whole')
        if price_elements:
            # Try to capture decimal values if present
            decimal_elements = soup.find_all('span', class_='a-price-fraction')
            if decimal_elements:
                price = price_elements[0].get_text().strip() + decimal_elements[0].get_text().strip()
            else:
                price = price_elements[0].get_text().strip()
            logging.info(f"Price found on Amazon: {price}")
            return price
        else:
            # Alternative price locations (for sales, promotions, etc.)
            alt_price_element = soup.find('span', class_='a-size-medium a-color-price priceBlockBuyingPriceString')
            if alt_price_element:
                price = alt_price_element.get_text().strip()
                logging.info(f"Alternative price found on Amazon: {price}")
                return price

    elif site_name == 'Flipkart':
        # Check the price element for Flipkart
        price_element = soup.find(class_='Nx9bqj')
        if price_element:
            price = price_element.get_text().strip()
            logging.info(f"Price found on Flipkart: {price}")
            return price

    logging.warning(f"Price not found on {site_name}.")
    return None


def clean_price(price_str):
    try:
        price = price_str.replace('₹', '').replace(',', '').strip()
        return float(price)
    except ValueError as e:
        logging.error(f"Error converting price '{price_str}': {e}")
        return None


def track_prices(product_name):
    product_urls = {
        'Amazon': f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}&ref=nb_sb_noss',
        'Flipkart': f'https://www.flipkart.com/search?q={product_name.replace(" ", "+")}'

    }

    lowest_price = float('inf')
    lowest_price_site = None
    lowest_price_url = None

    for site_name, url in product_urls.items():
        page = get_page(url)
        if page:
            price_str = parse_price(page, site_name)
            if price_str:
                price = clean_price(price_str)
                if price is not None:
                    # Display the logo and price without box
                    if site_name == 'Amazon':
                        st.image(amazon_logo, width=100)
                    elif site_name == 'Flipkart':
                        st.image(flipkart_logo, width=100)

                    st.write(f"{site_name} - Current price: ₹{price}")
                    logging.info(f"{site_name} - Current price: ₹{price}")

                    # Check for lowest price
                    if price < lowest_price:
                        lowest_price = price
                        lowest_price_site = site_name
                        lowest_price_url = url

    if lowest_price_site:
        st.write(f"\nBest Deal  : ₹{lowest_price} at {lowest_price_site}")
        st.write(f"[Link to product]({lowest_price_url})")
        logging.info(f"Best Deal: ₹{lowest_price} at {lowest_price_site} - Link: {lowest_price_url}")
    else:
        st.write("No prices found.")
        logging.warning("No prices found.")


# Streamlit UI
st.title('Deal Finder')

# Input for product name
product_name = st.text_input("Enter the product name")

if st.button('Find Deal'):
    if product_name:
        track_prices(product_name)
    else:
        st.write("Please enter a product name.")
