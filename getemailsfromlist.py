import requests
from bs4 import BeautifulSoup
import re

def scrape_email_addresses(urls):
    email_addresses = []

    for url in urls:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            email_tags = soup.find_all(href=re.compile(r'^mailto:'))

            for email_tag in email_tags:
                email = email_tag['href'][7:]  # Extract the email address
                email_addresses.append(email)
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {url}: {e}")

    return email_addresses

# Example usage
urls = [
    'https://www.example1.com',
    'https://www.example2.com',
    'https://www.example3.com'
]
emails = scrape_email_addresses(urls)

# Print the scraped email addresses
for email in emails:
    print(email)
