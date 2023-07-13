import requests
from lxml import etree

url = 'https://www.cargiant.co.uk/search/bmw/all'
response = requests.get(url)
html_content = response.content

# Parse the HTML content using lxml
tree = etree.HTML(html_content)

# Use XPath to select the desired elements with the data-results attribute
elements = tree.findall('.//*[@data-results]')

# Print the content of each selected element
for element in elements:
    print(etree.tostring(element, pretty_print=True).decode())
