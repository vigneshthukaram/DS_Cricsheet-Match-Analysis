import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import zipfile

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# URL of the CricSheet matches page
url = "https://cricsheet.org/matches/"

try:
    # Open the page
    driver.get(url)

    # Locate all links on the page
    match_links = driver.find_elements(By.TAG_NAME, "a")

    # Check for links containing '/downloads', 'json', 'zip', and specific formats (t20s, tests, odis)
    formats = ["t20s", "tests", "odis"]
    zip_links = []

    for link in match_links:
        href = link.get_attribute("href")
        if href and "/downloads" in href and "json" in href and "zip" in href:
            for fmt in formats:
                if fmt in href.lower():  # Check if the format is in the URL
                    zip_links.append(href)
                    break

    # Download and extract each ZIP file
    for zip_link in zip_links:
        print(f"Found ZIP link: {zip_link}")

        # Download the ZIP file
        response = requests.get(zip_link)
        zip_filename = os.path.basename(zip_link)

        with open(zip_filename, "wb") as zip_file:
            zip_file.write(response.content)
        print(f"Downloaded ZIP file: {zip_filename}")

        # Extract the contents of the ZIP file
        extract_dir = f"extracted_{os.path.splitext(zip_filename)[0]}"
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(zip_filename, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
            print(f"Extracted contents to: {extract_dir}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
