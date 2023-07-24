# script.py

import sys
import os

# Add the parent directory (project) to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from modules.webscrape_cargiant_class import WebScraperCargiant

scrape = WebScraperCargiant(driver="chrome", keepalive=False)

scrape.search_for_manufacturer(manufacturer="BMW")
scrape.search_for_manufacturer("Mercedes")
scrape.print_data()