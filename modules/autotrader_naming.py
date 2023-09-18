from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chromium.options import ChromiumOptions as ChromiumOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from fuzzywuzzy import fuzz

#get autotrader variables for naming


class autotrader_naming:
    def __init__(self, driver: str):
        self.driver = driver
        

    def selenium_setup(self):
        if self.driver == "safari":
            safari_options = SafariOptions()
            self.driver = webdriver.Safari(options=safari_options)
        
        elif self.driver == "chrome":
            chrome_options = ChromeOptions()
            # chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--window-size=1920,1200")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--start-minimized")
            self.driver = webdriver.Chrome(options=chrome_options)
        elif self.driver == "chromium":
            chromium_options = ChromiumOptions()
            chromium_options.add_argument("--no-sandbox")
            chromium_options.add_argument("headless")
            chromium_options.add_argument("--crash-dumps-dir=/tmp")
            chromium_options.add_argument("--disable-gpu")
            chromium_options.add_argument("--disable-dev-shm-usage")
            chromium_options.add_argument("--window-size=800,600")
            chromium_options.add_argument("--ignore-certificate-errors")
            chromium_options.add_argument("--disable-extensions")
            chromium_options.add_argument("--start-minimized")
            self.driver = webdriver.Chrome(options=chromium_options)
        
        elif self.driver == "firefox":
            firefox_options = FirefoxOptions()
            firefox_options.headless = True
            firefox_options.add_argument("--window-size=1920,1200")
            firefox_options.add_argument("--ignore-certificate-errors")
            firefox_options.add_argument("--start-minimized")
            self.driver = webdriver.Firefox(options=firefox_options)
    def get_car_makes(self):
        self.selenium_setup()
        driver = self.driver
        url = "https://www.autotrader.co.uk/car-search?postcode=TR17%200BJ"
        driver.get(url)


        #click button
        make_button_section = driver.find_element(By.CSS_SELECTOR, '[data-testid="toggle-facet-make"]')

        make_button_section.find_element(By.CSS_SELECTOR, '[data-testid="toggle-facet-button"]').click()
        #get all makes
        make = driver.find_element(By.CSS_SELECTOR, '[data-section="make"]')
        all_makes = make.find_element(By.XPATH, "//h3[text()='All makes']/following-sibling::ul")


        manufacturers = []
        makes = all_makes.find_elements(By.XPATH, ".//li/button/span[1]")

        for car_makes in makes:
            manufacturers.append(car_makes.text)

        return manufacturers

    def get_car_models(self, make):
        self.selenium_setup()
        driver = self.driver
        make = make.replace(" ","%20")
        url = f"https://www.autotrader.co.uk/car-search?make={make}&postcode=TR17%200BJ"
        print(f"DEBUG using {url}", flush=True)
        driver.get(url)

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
    def translate_modelname_to_autotrader(self, car_make, input_string, custom_data: None):
        """
        Takes a model name and Returns a model name which is defined in autotrader. This shouldn be used in the "aggregatedTrim" with just "Make" to scrape prices
        ARG
        car_make: type(str) eg. BMW
        input_model_name eg. 320D

        returns 320d 
        """
        if custom_data:
            car_models = custom_data
        else:
            car_models = self.get_car_models(make=car_make)
        
        best_match = None
        best_score = 0 
        score_data = []
        for car_model_name in car_models:
            similarity_score = fuzz.ratio(input_string.lower(), car_model_name.lower())

            
            #BMW models algo adjust
            if(car_make == "BMW"):
                if re.match(r"(\d\s*series|series\s*\d)", car_model_name.lower()): ##boost BMW [number] series scores
                    similarity_score += 50
                ######
                input_numeric_part_series = re.search(r"\b(\d+)\b\s[S-s]eries\b", car_model_name.lower())
                car_model_numeric_part = re.search(r"\d\w\w\w",  input_string.lower())
                if input_numeric_part_series and car_model_numeric_part: # select the words if the match numeric part eg. 1 series == 112i 
                    if input_numeric_part_series.group(0)[0] == car_model_numeric_part.group(0)[0]: # this gets the first digit
                        similarity_score += 30


                        # Mercedes
            if(car_make == "Mercedes") : # Bump up the [letter] Class
                input_name_letter_part = re.search(r"([a-zA-Z]\d\d)|([a-zA-Z]{3})", input_string.lower())
                car_model_name_letter_part = re.search(r"[a-zA-Z]{1,3}\s\b[cC]lass\b", car_model_name.lower())
                if input_name_letter_part and car_model_name_letter_part:
                    if input_name_letter_part.group(0)[0] == car_model_name_letter_part.group(0)[0]:
                        similarity_score += 80
                    #bump down EQE  [Q] [part car model names as they are electric variants
                        if input_name_letter_part.group(0)[1] == "q":
                            similarity_score -= 30

                #3 letter classees like bump up CLA-> to CLA class
                input_name_cla = re.search(r"\b[a-zA-Z]{3}\b", input_string.lower())
                car_model_cla = re.search(r"[a-zA-Z]{3}\s\b[cC]lass\b", car_model_name.lower())
                if input_name_cla and car_model_cla:
                                    #for bump up GLE (the E ) part
                    if input_name_cla.group(0)[0] == "g":
                        #if the E part matches the first part of inputname
                        if input_name_cla.group(0)[0] ==  car_model_name_letter_part.group(0)[2]:
                            similarity_score += 50 
                    elif input_name_cla.group(0)[0] == car_model_name_letter_part.group(0)[0]:
                        similarity_score += 50


            # functions getting the top score
            if similarity_score > best_score:
                best_match = car_model_name
                best_score = similarity_score
            score_data.append({car_model_name : similarity_score})


        print(f"DEBUG: Best match was {input_string}->{best_match} with score {best_score}")
        #more diagnostic print(f"DEBUG: Best match was {input_string}->{best_match} with score {best_score}\n with {score_data} \n")

        return best_match
        
