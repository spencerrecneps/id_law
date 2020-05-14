#
# Defines classes for each level of the hierarchy
#
# Title
#   Chapter
#     Section
#
from lxml import html, etree
import requests

root_url = r"https://legislature.idaho.gov"

class Title:
    def __init__(self, node):
        """
        args

        node -- the HTML node of the table row representing this title
        """
        a = node.xpath("//tr/td/a")[0] # gets the anchor node
        self.heading = a.text.strip()
        self.url = root_url + a.attrib["href"]
        self.name = node.xpath("//tr/td")[2].text.strip() # gets the heading from the third cell in the row
        print(self.name)

        # load page and traverse chapters
        page = requests.get(self.url)
        tree = html.fromstring(page.content)
        self.chapters = list()
        for html_node in tree.xpath("//tr/td/a[contains(text(),'CHAPTER')]/../.."): # grabs the table rows for all <a> tags containing the word CHAPTER
            # THIS DOESN'T ACCOUNT FOR REPEALED CHAPTERS. NEED TO ADD
            # (MAYBE SWITCH TO SELECTING td DIRECTLY AND THEN SEARCHING FOR a IF IT'S THERE?)
            chapter = etree.ElementTree(html_node)
            self.chapters.append(Chapter(chapter))

class Chapter:
    def __init__(self, node):
        """
        args

        node -- the HTML node of the table row representing this chapter
        """
        a = node.xpath("//tr/td/a")[0] # gets the anchor node
        self.heading = a.text.strip()
        self.url = root_url + a.attrib["href"]
        self.name = node.xpath("//tr/td")[2].text.strip() # gets the heading from the third cell in the row
        print(".."+self.name)

        # load page and traverse sections
        page = requests.get(self.url)
        tree = html.fromstring(page.content)
        self.sections = list()
        # for html_node in tree.xpath("//tr/td/a/../.."): # grabs the table rows for all <a> tags
        for html_node in tree.xpath("//tr/td/a[contains(text(),'-')]/../.."): # grabs the table rows for all <a> tags containing the word CHAPTER
            # THIS DOESN'T ACCOUNT FOR REPEALED SECTIONS. NEED TO ADD
            # (MAYBE SWITCH TO SELECTING td DIRECTLY AND THEN SEARCHING FOR a IF IT'S THERE?)

            section = etree.ElementTree(html_node)
            self.sections.append(Section(section))

class Section:
    def __init__(self, node):
        """
        args

        node -- the HTML node of the table row representing this section
        """
        a = node.xpath("//tr/td/a")[0] # gets the anchor node
        self.heading = a.text.strip()
        self.url = root_url + a.attrib["href"]
        self.name = node.xpath("//tr/td")[2].text.strip() # gets the heading from the third cell in the row
        print("...."+self.name)

        # load page and traverse sections
        self.subsections = list()
