from selenium import webdriver
import time
import bs4
from selenium.webdriver.common.by import By
import re
#get autotrader variables for naming

driver = webdriver.Safari()
def get_car_makes(): 
    url = "https://www.autotrader.co.uk/car-search?postcode=TR17%200BJz"
    driver.get(url)
    time.sleep(5)
    #click button
    driver.find_element(By.CSS_SELECTOR, '[data-testid="toggle-facet-button"]').click()
    #get all makes
    make = driver.find_element(By.CSS_SELECTOR, '[data-section="make"]')
    all_makes = make.find_element(By.XPATH, "//h3[text()='All makes']/following-sibling::ul")


    manufacturers = []
    makes = all_makes.find_elements(By.XPATH, ".//li/button/span[1]")

    for car_makes in makes:
        manufacturers.append(car_makes.text)

    return manufacturers

def get_car_models(make):
    make = make.replace(" ","%20")
    url = f"https://www.autotrader.co.uk/car-search?make={make}&postcode=TR17%200BJ"
    print(f"DEBUG using {url}", flush=True)
    driver.get(url)
    time.sleep(5)
    #click button
    model_button_section = driver.find_element(By.CSS_SELECTOR, '[data-testid="toggle-facet-model"]')
    model_button = model_button_section.find_element(By.CSS_SELECTOR, '[data-testid="toggle-facet-button"]').click()
    #get all models
    models = driver.find_element(By.CSS_SELECTOR, '[data-section="model"]')
    all_models_ul = models.find_element(By.XPATH, '//*[@id="model-facet-panel"]/section/div[2]/div/ul')
    all_model = all_models_ul.find_elements(By.XPATH, ".//li")

    pattern = r"(?<!\()\b.*?(?=\()"
    models = []
    for model in all_model:
        model_name_without_brackets = re.match(pattern, model.text)
        models.append(model_name_without_brackets.group(0))
    return models


print(get_car_makes(), flush=True)
print(get_car_models("Audi"))