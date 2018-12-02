#
# scrapes the main website recursively
#
from lxml import html, etree
import requests
from classes import Title

start_url = r"https://legislature.idaho.gov/statutesrules/idstat/"

page = requests.get(start_url)
tree = html.fromstring(page.content)

titles = list()
for html_node in tree.xpath("//tr/td/a[contains(text(),'TITLE')]/../.."): # grabs the table rows for all <a> tags containing the word TITLE
    title = etree.ElementTree(html_node)
    titles.append(Title(title))
