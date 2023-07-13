from webscrape_cargiant_class import webscrape_cargiant


template = webscrape_cargiant()
template.getCarMakes()

bmw = webscrape_cargiant("bmw")
mercedes = webscrape_cargiant("mercedes")
lexus = webscrape_cargiant("lexus")
voltswagen = webscrape_cargiant("Volkswagen")
bmw.printData()
mercedes.printData()
lexus.printData()
voltswagen.printData()


bmwsearch = bmw.searchDataForCar("Model", "118D")
mercedessearch = mercedes.searchDataForCar("Body Type", "Hatch")