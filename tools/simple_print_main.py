from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

# Set up the Selenium WebDriver
driver = webdriver.Safari()

# Send a GET request to the website
url = 'https://www.cargiant.co.uk/search/bmw/all'  # Replace with the URL of the website you want to scrape

webpage = driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

results = soup.find_all('div', )


car_listing_items = driver.find_elements(By.CSS_SELECTOR, "div.car-listing-item")

for item in car_listing_items:
    # Process each car listing item
   price = item.find_element(By.CSS_SELECTOR, "div.price-block__price")
   model = item.find_element(By.CSS_SELECTOR, "span.title__main.set-h3")
   details = item.find_element(By.CSS_SELECTOR, "span.text-content")
   year =  item.find_element(By.CSS_SELECTOR, "span.title__sub__plate")                            
   print("Car = " + model.text)
   print("Price = " + price.text)
   print("Year = " + year.text.replace(",", ""))
   print("Details = " + details.text.strip() + "\n", flush=True)


driver.quit()

