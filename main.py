from webscrape_cargiant import webscrape_cargiant


template = webscrape_cargiant()
template.getCarMakes()

bmw = webscrape_cargiant("bmw")
mercedes = webscrape_cargiant("mercedes")
bmw.printData()
mercedes.printData()
bmwsearch = bmw.searchDataForCar("Model", "118D")
mercedessearch = mercedes.searchDataForCar("Body Type", "Hatch")