import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.olx.in/items/q-car-cover"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get(url)

try:
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li[data-aut-id='itemBox3']")))
    print("Listings container found.")

    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3) 

    page_source = driver.page_source

finally:
    driver.quit()

soup = BeautifulSoup(page_source, 'html.parser')

listings = soup.find_all('li', {'data-aut-id': 'itemBox3'})

print(f"Found {len(listings)} listings")

results = []

if listings:
    for listing in listings:
        title_element = listing.find('span', {'data-aut-id': 'itemTitle'})
        title = title_element.text.strip() if title_element else 'N/A'

        price_element = listing.find('span', {'data-aut-id': 'itemPrice'})
        price = price_element.text.strip() if price_element else 'N/A'

        location_element = listing.find('span', {'data-aut-id': 'item-location'})
        location = location_element.text.strip() if location_element else 'N/A'

        link_element = listing.find('a', href=True)
        link = "https://www.olx.in" + link_element['href'] if link_element else 'N/A'

        results.append({
            'Title': title,
            'Price': price,
            'Location': location,
            'URL': link
        })

if results:
    df = pd.DataFrame(results)
    df.to_csv('olx_car_cover_results.csv', index=False, encoding='utf-8')
    print("Scraping complete. Results saved to olx_car_cover_results.csv")
else:
    print("No data was scraped. While the main listing selector is correct, the internal selectors for title/price might need updating or the page has anti-scraping measures.")

