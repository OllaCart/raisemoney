import csv
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

if __name__ == '__main__':
    # Read URLs from a CSV file
    csv_filename = 'urls.csv'  # Replace with your CSV filename
    urls = []

    with open(csv_filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            urls.extend(row)

    # Call the scrape_email_addresses function with the extracted URLs
    emails = scrape_email_addresses(urls)

    # Print the scraped email addresses
    for email in emails:
        print(email)
