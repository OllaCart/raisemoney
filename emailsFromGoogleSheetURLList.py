import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import requests
from bs4 import BeautifulSoup

# Set up Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)

def extract_urls_from_sheet(sheet_name, url_column):
    sheet = client.open(sheet_name).sheet1  # Open the specified sheet
    urls = sheet.col_values(url_column)  # Retrieve all values from the specified column

    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    extracted_urls = []
    for url in urls:
        match = re.search(url_pattern, url)
        if match:
            extracted_urls.append(match.group())

    return extracted_urls

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
    # Extract URLs from Google Sheets
    sheet_name = 'YourSheetName'
    url_column = 1  # Assuming URLs are in the first column (column A)
    urls = extract_urls_from_sheet(sheet_name, url_column)

    # Call the scrape_email_addresses function with the extracted URLs
    emails = scrape_email_addresses(urls)

    # Write the emails to a file
    filename = f"{sheet_name}_emails.txt"
    with open(filename, 'w') as file:
        file.write('\n'.join(emails))

    print(f"Emails written to {filename}")
