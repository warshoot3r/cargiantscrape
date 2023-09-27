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
            return webdriver.Safari(options=safari_options)
        
        elif self.driver == "chrome":
            # import logging
            # logging.basicConfig(level=logging.ERROR)
            chrome_options = ChromeOptions()
            from fake_headers import Headers

            header = Headers(
                browser="chrome",  # Generate only Chrome UA
                os="win",  # Generate only Windows platformd
                headers=False # generate misc headers
            )
            customUserAgent = header.generate()['User-Agent']

            chrome_options.add_argument(f"user-agent={customUserAgent}")
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--start-minimized")
            chrome_options.add_argument("--disable-default-apps")
            chrome_options.add_argument("--disable-features=Translate")
            chrome_options.add_argument("--disable-client-side-phishing-detection")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--disable-component-extensions-with-background-pages")
            chrome_options.add_argument("--disable-ipc-flooding-protection")
            chrome_options.add_argument("--disable-hang-monitor")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--enable-automation")
            chrome_options.add_argument("--disable-background-networking")
            return webdriver.Chrome(options=chrome_options)
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
            return webdriver.Chrome(options=chromium_options)
        
        elif self.driver == "firefox":
            firefox_options = FirefoxOptions()
            firefox_options.headless = True
            firefox_options.add_argument("--window-size=1920,1200")
            firefox_options.add_argument("--ignore-certificate-errors")
            firefox_options.add_argument("--start-minimized")
            return webdriver.Firefox(options=firefox_options)

        
    def handle_cookie_prompt(self, driver: webdriver.Remote ):
        #handles cookie prompt
        wait = WebDriverWait(driver=driver, timeout=10)
        try:    
                wait.until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
                cookie_prompt_iframe = driver.find_elements(By.TAG_NAME, "iframe")
                if len(cookie_prompt_iframe) == 2: 
                            driver.switch_to.frame(cookie_prompt_iframe[1].get_attribute("id"))
                            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[title="Accept All"]')))
                            cookie_button = driver.find_element(By.CSS_SELECTOR, 'button[title="Accept All"]')
                            cookie_button.click()
                            print("VERBOSE: Clicked cookie prompt.")    
                            driver.switch_to.default_content()

        except exceptions.NoSuchElementException as e:
            print(f"No Element Exception while setting cookies. {e}", flush=True)
            return
        
        except exceptions.TimeoutException as e:
            print(f"Timeout Exception when accepting cookies {e}", flush=True)
            return
              
        
    def get_car_makes(self):
        
        driver = self.selenium_setup()
        url = "https://www.autotrader.co.uk/car-search?postcode=TR17%200BJ"
        driver.get(url)
        self.handle_cookie_prompt(driver=driver)
        wait = WebDriverWait(driver=driver, timeout=10)
        #click button
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="toggle-facet-make"]')))



        #get all makes  
      
      
        attempts = 0
        while True:
            try:
                model_variant_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="toggle-facet-make"]')))
                model_variant_button.click()
                print("DEBUG: Clicked on Make pane", flush=True)
                # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[id="model-variant-facet-panel"]')))
                wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[id="make-facet-panel"]')))
                break
            except exceptions.TimeoutException:
                print("DEBUG: Element is not visible yet", flush=True)
                time.sleep(1)
                attempts += 1
            except:
                print("Error occured on clicking the Model Variants button", flush=True)
                return
            if attempts >= 10:
                print(f"Failed to get car makes for {url}", flush=True)
                return

        wait.until(EC.visibility_of_all_elements_located(( By.CSS_SELECTOR, '[data-section="make"]')))
        make_section =  driver.find_element(By.CSS_SELECTOR, '[data-section="make"]')
        wait.until(EC.visibility_of_all_elements_located(( By.CSS_SELECTOR, '[data-gui="filters-list-filter-name"]')))
        make_data = make_section.find_elements(By.CSS_SELECTOR, '[data-gui="filters-list-filter-name"]')
                        
        manufacturers = []

        for car_makes in make_data:
            print(car_makes.text, flush=True)
            manufacturers.append(car_makes.text)
        return manufacturers
  
        

    def get_car_models(self, make):
       
        driver = self.selenium_setup()
        make = make.replace(" ","%20")
        url = f"https://www.autotrader.co.uk/car-search?make={make}&postcode=TR17%200BJ"
        # print(f"DEBUG get car models using {url}", flush=True)
        wait = WebDriverWait(driver=driver, timeout=10)
        driver.get(url)
        self.handle_cookie_prompt(driver)
        #click button


        attempts = 0
        while True:
            try:
                model_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="toggle-facet-model"]')
                model_button.click()
                print("DEBUG: Clicked on Make Pane", flush=True)
                # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[id="model-variant-facet-panel"]')))
                wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[data-gui="filters-list-filter-name"]')))
                break
            except exceptions.TimeoutException:
                print("DEBUG: Element is not visible yet", flush=True)
                time.sleep(1)
                attempts += 1
            except:
                print("Error occured on clicking the Model Variants button", flush=True)
                return
            if attempts >= 5:
                print(f"Failed to get models for {url}", flush=True)
                return
  
        #inside the model variants da

        #get all odels
        models = driver.find_element(By.CSS_SELECTOR, '[data-section="model"]')
        
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'[data-section="model"]')))

        all_model = models.find_elements(By.CSS_SELECTOR, '[data-gui="filters-list-filter-name"]')

        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[data-gui="filters-list-filter-name"]')))

        # all_models_ul = models.find_element(By.XPATH, '//*[@id="model-facet-panel"]/section/div[2]/div/ul')
        
        # all_model = all_models_ul.find_elements(By.XPATH, ".//li")
     
        # pattern = r"(?<!\()\b.*?(?=\()"

        models = []
        for model in all_model:
            # print(model.text, flush=True)
            models.append(model.text)
        # for model in all_model:
        #     print(model.text, flush=True)
        #     model_name_without_brackets = re.match(pattern, model.text)
        #     if model_name_without_brackets:
        #         models.append(model_name_without_brackets.group(0))
        return models
    
    def translate_modelvariant_to_autotrader(self, car_make, car_model, input_string, custom_data = None):

        if custom_data:
            model_variants_from_model = custom_data
        else:
            model_variants_from_model = self.get_model_variant_from_model(car_model=car_model,make=car_make)
        best_match = None
        best_score = 0

        if model_variants_from_model:
            for car_variant in model_variants_from_model:

                similarity_score = fuzz.ratio(input_string.lower(), car_variant.lower())

                if similarity_score > best_score:
                    best_match = car_variant
                    best_score = similarity_score
                    
            if best_score < 60:
                print(f"DEBUG: Best match for variant  {input_string} lower than 60 certainty. Return nothing. {input_string}->{best_match} (score:{best_score})", flush=True)
                return 
            else:
                print(f"DEBUG: Best match for variant {input_string}->{best_match} (score:{best_score})", flush=True)
                return best_match
        else:
            print("DEBUG: No data from input. Can't return a best match", flush=True)
            return

    def translate_modelname_to_autotrader(self, car_make, input_string, custom_data = None):
        """
        Takes a model name and Returns a model name which is defined in autotrader. This shouldn be used in the "aggregatedTrim" with just "Make" to scrape prices
        ARG
        car_make: type(str) eg. BMW
        input_model_name eg. 320D

        returns 320d 
        """
        if custom_data:
            print("AUTOTRADER_CARDB: Using provided custom data", flush=True)
            car_models = custom_data
        elif car_make == "BMW":
            car_models = ['1602', '1 Series', '2002', '2 Series', '2 Series Active Tourer', '2 Series Gran Coupe', '2 Series Gran Tourer', '3 Series', '3 Series Gran Turismo', '4 Series', '4 Series Gran Coupe', '5 Series', '5 Series Gran Turismo', '6 Series', '6 Series Gran Coupe', '6 Series Gran Turismo', '7 Series', '8 Series', '8 Series Gran Coupe', 'Alpina B10', 'Alpina B3', 'Alpina B4', 'Alpina B4 Gran Coupe', 'Alpina B5', 'Alpina B6', 'Alpina B8 Gran Coupe', 'Alpina D3', 'Alpina D4', 'Alpina D4 Gran Coupe', 'Alpina D5', 'Alpina Roadster', 'Alpina Unspecified Models', 'Alpina XB7', 'Alpina XD3', 'E9', 'i3', 'i4', 'i5', 'i7', 'i8', 'Isetta', 'iX', 'iX1', 'iX3', 'M2', 'M3', 'M4', 'M5', 'M6', 'M6 Gran Coupe', 'M8', 'M8 Gran Coupe', 'X1', 'X2', 'X3', 'X3 M', 'X4', 'X4 M', 'X5', 'X5 M', 'X6', 'X6 M', 'X7', 'XM', 'Z1', 'Z3', 'Z3 M', 'Z4', 'Z4 M', 'Z8']
        elif car_make == "Mercedes" or  car_make == "Mercedes-Benz":
            car_models =  ['A Class', 'AMG', 'AMG GT', 'AMG GT 63', 'B Class', 'C Class', 'Citan', 'CL', 'CLA Class', 'CLC Class', 'CLK', 'CLS', 'E Class', 'EQA', 'EQB', 'EQC', 'EQE', 'EQS', 'EQV', 'eVito', 'G Class', 'GLA Class', 'GLB Class', 'GLC Class', 'GL Class', 'GLE Class', 'GLS Class', 'Maybach GLS Class', 'Maybach S Class', 'M Class', 'R Class', 'S Class', 'SE Class', 'SEC Series', 'SLC', 'SL Class', 'SLK', 'SLR McLaren', 'SLS', 'Sprinter', 'Traveliner', 'V Class', 'Viano', 'Vito', 'X Class']
        elif car_make == "Lexus":
            car_models = ['CT 200h', 'ES 300h', 'GS 250', 'GS 300', 'GS 430', 'GS 450h', 'GX', 'IS 200', 'IS 220d', 'IS 250', 'IS 300', 'IS F', 'LC 500', 'LFA', 'LS 400', 'LS 430', 'LS 460', 'LS 500h', 'LS 600h', 'NX 200t', 'NX 300h', 'NX 350h', 'NX 450h+', 'RC 200t', 'RC 300h', 'RC F', 'RX 200t', 'RX 300', 'RX 350', 'RX 350h', 'RX 400h', 'RX 450h', 'RX 450h+', 'RX 500h', 'RX L 450h', 'RX Unspecified', 'RZ 450e', 'SC 430', 'UX 250h', 'UX 300e']
        else:
            car_models = self.get_car_models(make=car_make)
        
        best_match = None
        best_score = 0 
        score_data = []

        if car_models: 
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
                if(car_make == "Mercedes") or (car_make == "Mercedes-Benz") : # Bump up the [letter] Class
                    input_name_letter_part = re.search(r"([a-zA-Z]\d\d)|([a-zA-Z]{3})", input_string.lower())
                    car_model_name_letter_part = re.search(r"[a-zA-Z]{1,3}\s\b[cC]lass\b", car_model_name.lower())
                    if input_name_letter_part and car_model_name_letter_part:
                        if input_name_letter_part.group(0)[0] == car_model_name_letter_part.group(0)[0]:
                            similarity_score += 80
                        #bump down EQE  [Q] [part car model names as they are electric variants
                            if input_name_letter_part.group(0)[1] == "q":
                                similarity_score -= 30

                    #3 letter model classes like bump up CLA-> to CLA class
                    input_name_cla = re.search(r"\b[a-zA-Z]{3}\b", input_string.lower())
                    car_model_cla = re.search(r"[a-zA-Z]{3}\s\b[cC]lass\b", car_model_name.lower())
                    if input_name_cla and car_model_cla:
                                        #for bump up GLE (the E ) part
                        if input_name_cla.group(0)[0] == "g":
                            #if the E part matches the first part of inputname
                            if input_name_cla.group(0)[0] ==  car_model_name_letter_part.group(0)[2]:
                                similarity_score += 50 
                        if input_name_cla.group(0)[0] == car_model_name_letter_part.group(0)[0]:
                            #if eg. the g in GLA match GLE Class
                            similarity_score += 50
 


                # functions getting the top score
                if similarity_score > best_score:
                    best_match = car_model_name
                    best_score = similarity_score
                score_data.append({car_model_name : similarity_score})
        else:
            print("DEBUG: No data from input. Can't return models", flush=True)
            return

        
        #more diagnostic print(f"DEBUG: Best match was {input_string}->{best_match} with score {best_score}\n with {score_data} \n", flush=True)
        if best_score < 60:
            print(f"DEBUG: Best match lower than 60 certainty. Return nothing. {input_string}->{best_match} (score:{best_score})", flush=True)
            return
        else:
            print(f"DEBUG: Best match for model {input_string}->{best_match} (score:{best_score})", flush=True)
            return best_match
        
    def get_model_variant_from_model(self, make, car_model):
        #may fix the nosuchelementexcepton
        make = make.replace(" ","%20")
        car_model = car_model.replace(" ", "%20")
        url = f"https://www.autotrader.co.uk/car-search?make={make}&model={car_model}&postcode=TR17%200BJ"
        # print(f"DEBUG using {url}", flush=True)
        driver = self.selenium_setup()
        wait = WebDriverWait(driver=driver, timeout=10)
        print(f"DEBUG: {url} Attempting to gather Model Variant", flush=True)
        driver.get(url)
        attempts = 0
        while True:
            models = []
            try:
                model_variant_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="toggle-facet-model-variant"]')))
                self.handle_cookie_prompt(driver)
                # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[id="model-variant-facet-panel"]')))
                wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="toggle-facet-button"]')))
                model_variant_button.click()
                print("Clicked on variant pane", flush=True)
                wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[data-section="aggregated_trim"]')))
                model_variant_data_section =  driver.find_element(By.CSS_SELECTOR, '[data-section="aggregated_trim"]')
                wait.until(EC.visibility_of_all_elements_located(( By.CSS_SELECTOR, '[data-gui="filters-list-filter-name"]')))
                model_variant_data = model_variant_data_section.find_elements(By.CSS_SELECTOR, '[data-gui="filters-list-filter-name"]')

                for model_variant in model_variant_data:
                    try :
                        models.append(model_variant.text)
                    except exceptions.StaleElementReferenceException:
                        print(f"DEBUG: Stale elementt retrieving model name")
                    except Exception as e:
                        print(f"DEBUG: Error occured extracting model name: {e}")
                        break
                print((models))
                return models
            except exceptions.TimeoutException:
                print(f"DEBUG: {car_model} is not visible yet", flush=True)
                driver.get(url)
                time.sleep(1)
                attempts += 1
            except exceptions.StaleElementReferenceException:
                print(f"DEBUG Stale element on model variant. Retrying", flush=True)
                driver.get(url)
                attempts +=1
            except Exception as e:
                print(f"Error occured on clicking the Model Variants button {e}", flush=True)
                driver.get(url)
                attempts +=1
            if attempts >= 5:
                print(f"Failed to get model variants for {url}", flush=True)
                return None
  
        #inside the model variants data table

       


    
# naming = autotrader_naming(driver="chrome")
# # print(naming.get_model_variant_from_model(make="BMW",car_model="1 Series"), flush=True)
# # print(naming.get_car_makes(), flush=True)
# # naming.get_car_models(make="BMW")
# # naming.translate_modelvariant_to_autotrader(car_make="BMW", car_model="1 Series", input_string="116D")
# #

# print(naming.get_car_models(make="Lexus"), flush=True)
# print(naming.get_car_models(make="Mercedes-Benz"), flush=True)
# print(naming.get_car_models(make="BMW"))