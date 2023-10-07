from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chromium.options import ChromiumOptions as ChromiumOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import concurrent.futures
class WebScraperCargiant:
    """
    A web scraper for collecting used car information from the Cargiant website.
    """

    driver = None
    
    def __init__(self, driver, keepalive, manufacturer_search=None):
        """
        Initializes the WebScraperCargiant object.

        Args:
            driver (str): The driver type to use for Selenium (safari, chrome, or firefox).
            keepalive (bool): Determines whether to keep the driver alive after data retrieval.
            manufacturer_search (str, optional): The manufacturer to search for. Defaults to None.
        """
        self.driver = str(driver)
        self.keepalive = bool(keepalive)
        self.data = pd.DataFrame()
        pd.set_option("display.max_colwidth", 100)
        pd.set_option('display.max_rows', None)
        self.length = self.data.shape[0]
        if manufacturer_search is not None:
            self.manufacturer_search = manufacturer_search
            self.url = "https://www.cargiant.co.uk/search/" + manufacturer_search + "/all"
            print("Setting the search to", self.url, flush=True)
        else: 
            self.url = "https://www.cargiant.co.uk/search/all"

    def initialize_driver(self) -> webdriver.Remote:
        """
        Initializes the Selenium driver based on the specified driver type.
        """
        if self.driver == "safari":
            safari_options = SafariOptions()
            return webdriver.Safari(options=safari_options)
        
        elif self.driver == "chrome":
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1200")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--start-maximized")
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
        
        elif self.driver == "firefox":
            firefox_options = FirefoxOptions()
            firefox_options.headless = True
            firefox_options.add_argument("--window-size=1920,1200")
            firefox_options.add_argument("--ignore-certificate-errors")
            firefox_options.add_argument("--start-minimized")
            return webdriver.Firefox(options=firefox_options)
        
        raise ValueError("ERROR Invalid Driver specified")

    def get_car_url_snapshot(self, url):
        '''
        Returns a screenshot in base64. 
        If INPUT array, return an array
        If single input ,return single base64 string
        
        INPUT 
            URL eg. https://www.cargiant.co.uk/car/BMW/330e/RO18UTU
            
            Returns Base64 encoded string
        '''
        driver = self.initialize_driver()

        if(isinstance(url, str)):
                driver.get(url=url)
                return driver.get_screenshot_as_base64()
        elif(isinstance(url, list)):
                data = list()
                for car in url:
                    driver.get(url=car)
                    screenshot = driver.get_screenshot_as_png()
                    data.append(screenshot)
                return data
        else:
            raise TypeError("Input must be either string or list")
        
        
        
        
    def get_car_details(self, url, debug=False):
        """
        Goes to car giant URL and then scrapes for the specifiations of car data
        ARGS: 
            URL : https://www.cargiant.co.uk/car/Suzuki/Celerio/LM67FFV"

        Returns:
        Example
        Model->Mercedes GLA.
        Engine_Variant->2.2 220d Sport Executive 4Matic DCT
        Mileage -> 80,215
        Doors -> 5
        Transmission -> Auto
        Colour -> Black
        Year -> 2017
        Body Type -> SUV
        Fuel Type -> Diesel
        Combined -> 58.9
        Urban -> 48.7
        Extra Urban -> 65.7
        CO2 Emissions -> 127 g/kg
        Service History -> TBA
        Last Service -> N/A
        Keepers -> 2
        Tax Band -> D - £165 PA
        MOT -> N/A
        Insurance Group (1-50) -> 27E
                
        
        """
        if self.check_reg_url_alive(FullRegistrationURL=url) is True:
            print(f"CG: {url} is dead. No details can be grabbed.", flush=True)
            return False 
        
        output = {}
        

        web_page_data = requests.get(url, allow_redirects=False)
        if not web_page_data.content:
            print(f"DEBUG: Couldn't get {url}", flush=True)
            return
        
        parsed_data = BeautifulSoup(web_page_data.content, "html.parser")
        data = parsed_data

        # Car title details
        car_title_details = parsed_data.find("div", class_="car-details-wrap__desc__title")

        # Check if the element was found before trying to extract text.
        if car_title_details:
            # Extract the text and strip any leading/trailing whitespace.
            car_detail_fields = car_title_details.get_text().strip().split("\n")
            model = car_detail_fields[0]
            engine_variant = car_detail_fields[1]
            output["model"] = model
            output["engine_variant"] = engine_variant

        all_table_data = parsed_data.find_all("li", class_="details-panel-item__list__item")
        # all other data dynamiclly
        if all_table_data:
            for data in all_table_data:
                field  = data.find("span")
                if len(field) == 1:
                        field_propety_name = field.get_text().strip().lower()
                        field_property_data = field.find_next_sibling().get_text().strip()
                        output[field_propety_name] = field_property_data

        if debug:
            print(f"Got {output['model']}", flush=True)
            for key, value in output.items():
                print(f"CARGIANT_MODULE: {key} -> {value}", flush=True)
            print('\n', flush=True)
        return output

    def print_number_of_cars(self):
        """
        Prints the number of cars scraped from cargiant
        """
        print(f"\n\nNumber of cars scraped from cargiant -> {self.length}\n\n", flush=True)

    def search_for_manufacturer(self, manufacturer, numberofpages=15):
        """
        Sets the search to a specific manufacturer. This does not save the generic model eg, 3 series
        Args:
                manufacturer (str): The manufacturer to search for.
                NumberOfPages(int): Defines how many pages to scrape
        Return:
                pull_new_data returns a panda table`

        """
        self.numberofpages = numberofpages
        self.manufacturer_search = manufacturer
        url = "https://www.cargiant.co.uk/search/" + manufacturer + "/all"
        print("Setting the search to", url, flush=True)
        self.pull_new_data(numberofpages=numberofpages, url=url)

    def search_for_manufacturer_with_bmw_or_mercedes(self, manufacturer, numberofpages=10, worker_threads=4 ):
        """
        Parallel pull. Sets the search to a specific manufacturer. This will save the generic model as "https://www.cargiant.co.uk/search/" + manufacturer "HERE" the  eg, 3 series
        Args:
                manufacturer (str): The manufacturer to search for.
                NumberOfPages(int): Defines how many pages to scrape
        Return:
                pull_new_data returns a panda table`

        """
        self.manufacturer_search = manufacturer
        if not(manufacturer == "BMW") and not(manufacturer == "Mercedes"):
            raise TypeError("Must be BMW or Mercedes")
        if manufacturer == "BMW":
            series = ["all-1-series", "all-2-series", "all-3-series", "all-4-series", "all-5-series", "all-6-series", "all-7-series"]
        elif manufacturer == "Mercedes":
            series = ["all-a-class", "all-b-class", "all-c-class", "all-e-class", "all-s-class"]
        
        self.parallel_pull_new_data(manufacturer=manufacturer, series_to_process=series, number_of_pages=numberofpages, worker_threads=worker_threads)
        return self.data
    def import_sqldb_data(self, data_frame):
        """
        Imports past data from a DataFrame.

        Args:
            data_frame (pd.DataFrame): The DataFrame containing past data to be imported.
        """
        print("Importing past data", flush=True)
        self.data = data_frame

    def get_car_makes(self):
        """
        Prints the list of car makes available on the Cargiant website.
        """
        driver = requests.get("https://www.cargiant.co.uk/search/")
        content = driver.content
        soup = BeautifulSoup(content, 'html.parser')
        makes = soup.find_all(id="Makes")
        print("Listing Car makes", flush=True)
        for item in makes:
            print(item.text, flush=True)


    def search_data_for_car(self, search_col, term):
        """
        Searches the data for a specific car based on the specified column and term.

        Args:
            search_col (str): The column name to search for.
            term (str): The term to be searched in the specified column.

        Returns:
            WebScraperCargiant: A new WebScraperCargiant object containing the search results.
        """
        if search_col not in self.data.columns.values:
            print(f"{search_col} must be one of:", flush=True)
            print(self.data.columns.values, flush=True)
            return

        pattern = re.escape(term)
        mask = self.data[search_col].apply(lambda x: bool(re.search(pattern, x)))
        model_retrieved = self.data[mask]
        
        print(f"\n\nReturning a search with: {search_col} -> {term}", flush=True)
        print(model_retrieved, flush=True)
        
        self.data = model_retrieved
        return self

    def pull_new_data(self, url, numberofpages=10):
    
        """
        Retrieves new car data from the Cargiant website and updates the DataFrame.

        """
        print(f"Pulling new data: {url}", flush=True)
        driver = self.initialize_driver()
        wait = WebDriverWait(driver, 20)
        driver.get(url)
        
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.car-listing-item")))
        car_listing_items_page_1 = driver.find_elements(By.CSS_SELECTOR, "div.car-listing-item")
        print(f"\nCurrently web scraping {self.manufacturer_search} cars on page 1", flush=True)
        self.extract_web_data(car_listing_items_page_1)
        # check if only 1 page here. we must stop if is only one. otherwise code below will scrape same page.
        page_count = driver.find_element(By.CSS_SELECTOR, "#TotalPages").get_attribute("value")#

        if page_count == "1":
            print(f"Stopping scraping as only 1 page", flush=True)
        
        else:
            for page in range(1,numberofpages):
                

                pages = driver.find_elements(By.CSS_SELECTOR , '[data-paging-pages-template="page"]')
                print(f"\nCurrently web scraping {self.manufacturer_search} cars on page {page+1}.", flush=True)
                try:
                    driver.execute_script("arguments[0].click()", pages[page]) # click page
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.car-listing-item")))
                    current_page = driver.find_elements(By.CSS_SELECTOR, "div.car-listing-item")
                    self.extract_web_data(current_page)
                    driver.find_element(By.CSS_SELECTOR , '[data-paging-pages-template="next"]') #check if page has a next button. NoSuchElementException is raised and page scrape stops
                except NoSuchElementException:
                        print("Reached end of pages", flush=True)
                        self.stopwebdriver(driver)
                        return
                except IndexError:
                        print("Nothing to scrape", flush=True)
                        self.stopwebdriver(driver)
                        return
        
   
    def extract_web_data(self, scraped_data):
        
       
        table_template = {
            "Manufacturer": [],
            "Car Status": [],
            "Engine Size": [],
            "Model": [],
            "Model Variant": [],
            "Year": [],
            "Price": [],
            "Body Type": [],
            "Transmission": [],
            "Fuel": [],
            "Color": [],
            "Mileage": [],
            "Doors": [],
            "Reg": [],
            "URL": []
        }

        tf = pd.DataFrame(table_template)
        
        for item in scraped_data:
            # Extracting car details
            
            price_get = item.find_element(By.CSS_SELECTOR, "div.price-block__price").text
            price = re.sub("[^0-9.]", "", price_get)
            model = item.find_element(By.CSS_SELECTOR, "span.title__main.set-h3").text
            model_variant = item.find_element(By.CSS_SELECTOR, "span.title__sub.set-h4").text.split(',')[0].strip()
            model_split = re.split(r'(^\s*[\w]+)\b', model)
            model_split = [item for item in model_split if item]
            car_manufacturer = model_split[0]
            model_name = model_split[1].strip()
            #PATCHING engine size
            engine_size = None # preventatibv measure incase nothing returned
            get_engine_size_regex = r"(\d+\.\d+)(?:\s(.*))?" # r"(\d+.\d+)\s(.*)"
            if model_variant:
                get_engine_size_regex_search = re.search(pattern=get_engine_size_regex, string=model_variant)    
                

            if get_engine_size_regex_search:
                if get_engine_size_regex_search.group(2) == None:
                    engine_size = get_engine_size_regex_search.group(1)
                    model_variant = None
                else:
                    engine_size = get_engine_size_regex_search.group(1)
                    model_variant = get_engine_size_regex_search.group(2)

            if car_manufacturer == "Mercedes":           
                if model_variant:
                    remove_d_regex = r"([dD])\s(.*)"
                    remove_d_regex_search = re.search(pattern=remove_d_regex, string=model_variant)
                    if remove_d_regex_search:
                        model_name = model_name + remove_d_regex_search.group(1)
                        model_variant = remove_d_regex_search.group(2)
                    cla_gla_models_regex = r"(\d{3})\s(.*)"
                    cla_gla_models_regex_search = re.search(pattern=cla_gla_models_regex, string=model_variant)
                    if cla_gla_models_regex_search:
                        model_name = model_name + cla_gla_models_regex_search.group(1) 
                        model_variant = cla_gla_models_regex_search.group(2)

                    #fixing mercedes diesel cars 220 becomes 220d
                 
            #PATCHING MODELS column
            elif car_manufacturer == "Lexus":# replace the UX becomes -> UX 250h to the model column
                three_number_and_one_letter_regex = r"(\d{3}\S)\s(.*)|(\d{3}\S)"
                if model_variant:
                    model_part_search =  re.search(three_number_and_one_letter_regex, string=model_variant)
                    if model_part_search:
                        print(model_part_search.groups())
                        if model_part_search.group(1) is None and model_part_search.group(2) is None and model_part_search.group(3) is not None:
                            model_name = model_name + model_part_search.group(3)
                            model_variant = None
                            print(f"DEBUG: 1. Match {model_name} ->> {model_variant}", flush=True)
                        elif model_part_search.group(1) is not None and model_part_search.group(2) is not None and model_part_search.group(3) is None:
                            model_variant = model_part_search.group(2)
                            model_name = model_name + model_part_search.group(1)
                            print(f"DEBUG: 2. Match {model_name} ->> {model_variant}", flush=True)

                        else:
                            print("DEBUG: Regex for Lexus not matched", flush=True)
                        

            elif model_name == "2 Series":# replace the 2 Series becomes -> 220d to the model column
                three_number_and_one_letter_regex = r"(\d{3}[a-zA-z])"
                if model_variant:
                    model_part_search =  re.search(three_number_and_one_letter_regex, string=model_variant)
                    if model_part_search:
                        model_name = model_part_search.group(0)
                        model_variant_split = re.sub(three_number_and_one_letter_regex, '' , string=model_variant).split()
                        model_variant = " ".join(model_variant_split)
                        print(f"CARGIANT_MODULE: Replaced model: {model}->{model_name}. Model variant: {model_variant}",flush=True)
                    else:
                        model_name = model_split[1].strip()
            print(f"DEBUG: {model} -> {model_variant} -> {engine_size}  ")

                # finish patching models

            year_get = item.find_element(By.CSS_SELECTOR, "span.title__sub__plate").text.replace(",", "")
            year = re.sub(r"(\d{4}).*", r"\1" , year_get)
            link = item.find_element(By.CSS_SELECTOR, "a.car-listing-item__details.split-half")
            car_link = link.get_attribute("HREF")
            car_reg = (re.split(r"[/\\](?=[^/\\]*$)", car_link))[1]

            details = item.find_element(By.CSS_SELECTOR, "span.text-content").text.strip()
            details_split = details.split(', ')
            DoorsAndType, Transmission, Fuel, Color, mileage_get = details_split
            mileage = re.sub("[^0-9.]", "" , mileage_get)
            try:
                car_status_get =  item.find_element(By.CSS_SELECTOR, "span.caption-block").text
                if(car_status_get == "SOLD TODAY"):
                    car_status = "Sold"
                elif(car_status_get == "RESERVED"):
                    car_status = "Reserved"
                elif(car_status_get == "AVAILABLE"):
                    car_status = "Available"
                else: 
                    car_status = car_status_get
                print(f"VERBOSE: {model_name} | {car_reg} saved as {car_status}", flush=True)
            except NoSuchElementException:
                car_status = "Available"
                print(f"VERBOSE: {model_name} | {car_reg} status is empty. Setting status to {car_status}", flush=True)

            DoorsAndType_split = re.split(r"\d\s(?=\s)", DoorsAndType)

            number_doors = ""
            body_type = ""
            for item in DoorsAndType_split:
                if re.match(r'\d', item):
                    number_doors, body_type = re.split(r'(?<=\d)\s...', item)
                else:
                    body_type = item
            
            if not number_doors:
                number_doors = "N/A"



            new_row = {
                "Manufacturer": car_manufacturer,
                "Model": model_name,
                "Model Variant": model_variant,
                "Year": year,
                "Engine Size": engine_size,
                "Details": details,
                "Price": price,
                "Body Type": body_type,
                "Doors": number_doors,
                "Transmission": Transmission,
                "Fuel": Fuel,
                "Color": Color,
                "Mileage": mileage,
                "URL": car_link,
                "Reg": car_reg,
                "Car Status": car_status
            }

            i = len(tf) + 1
            tf.loc[i] = new_row
        
        if self.data.empty:
            print("VERBOSE: No existing data. Scraped data is database ", flush=True)
            self.data = tf
            self.length = tf.shape[0]
        else:
            self.data = pd.concat([self.data.reset_index(drop=True), tf.reset_index(drop=True)])
            print("VERBOSE: Appended to self.data ", flush=True)
            self.length = self.data.shape[0]
            print(f"DEBUG: Appended to scrapeDB.", flush=True)
           
        # if not self.keepalive:
        #     driver.quit()
        
        print(f"Data successfully pulled {tf.shape[0] } cars", flush=True)
    def parallel_pull_new_data(self, series_to_process, manufacturer=None, number_of_pages=10, worker_threads=4):
            """
            concurrently pull cargiant cars with multiple urls. 
            "https://www.cargiant.co.uk/search/"+  manufacturer + "/" + series_name
            
            Inputs:
                - manufactuere type(str) eg. BMW
                - series name  type(array) eg. all-1-series
                - worker threads = number of parallel workers scraping at same time
            URL is created to be an array like https://www.cargiant.co.uk/search/BMW/all-6-series

            Returns:
                database
            
            """
            print(f"VERBOSE: Parallel Pull started. using {worker_threads} threads", flush=True)
            with concurrent.futures.ThreadPoolExecutor(worker_threads) as executor:
                futures = []

                for series_name in series_to_process:
                    url = "https://www.cargiant.co.uk/search/"+  manufacturer + "/" + series_name
                    future = executor.submit(self.pull_new_data, url, number_of_pages)
                    futures.append(future)

                # Wait for all futures to complete
                concurrent.futures.wait(futures)

                # If you want to access the results from the futures, you can iterate through futures and retrieve results
                for future in futures:
                    result = future.result()
                    print(f"Finished a pulling a parallel scrape", flush=True)
                    # Process the result as needed
        
    def stopwebdriver(self, driver):
        """
        Closes the browser and Kills the web driver.
        """
        driver.close()
        driver.quit()
        #Force killing the processes
        
    def check_reg_url_alive(self, FullRegistrationURL):
        """
        Returns true if reg url is alive. Used with DB to move to sold database
        Args:
        takes a single variable URL(str) eg. https://www.cargiant.co.uk/car/Lexus/CT-200h/YD67PCX
        """

        # check if car giant is alive 
        main_website = requests.get("https://www.cargiant.co.uk", allow_redirects=True)
        if main_website.ok:
            get_reg_url = requests.get(FullRegistrationURL, allow_redirects=True)
            if get_reg_url.url == "https://www.cargiant.co.uk/":
                print(f"Link return {get_reg_url.url}. {FullRegistrationURL} likely sold.", flush=True)
                return True
            else:
                print(f"{FullRegistrationURL} is not sold . Nothing to do", flush=True)
                return False
            
        else:
            return ConnectionRefusedError
