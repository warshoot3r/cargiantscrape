from selenium import webdriver
from selenium.webdriver.common.by import By 
import time

driver = webdriver.Chrome()
url = "https://www.autotrader.co.uk/car-search?postcode=TR17%200BJ&make=BMW&model=1%20series&minimum-mileage=57637&maximum-mileage=63637&year-from=2016&year-to=2017"


driver.get(url)
time.sleep(5)

#handles cookie prompt
try:
    cookie_prompt_iframe = driver.find_elements(By.TAG_NAME, "iframe")[1].get_attribute("id")
    print("VERBOSE: Clicked cookie prompt.")    
    if cookie_prompt_iframe:
        driver.switch_to.frame(cookie_prompt_iframe)
        cookie_button = driver.find_element(By.CSS_SELECTOR, 'button[title="Accept All"]')
        cookie_button.click()
except:
    print("No cookie prompt.", flush=True)

time.sleep(5)

driver.close()
