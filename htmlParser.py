from html.parser import HTMLParser
from bs4 import BeautifulSoup

# class MyHTMLParser(HTMLParser):
#     def handle_starttag(self, tag, attrs):
#         print("Encountered a start tag:", tag)

#     def handle_endtag(self, tag):
#         print("Encountered an end tag :", tag)

#     def handle_data(self, data):
#         print("Encountered some data  :", data)

with open('test.html') as file:
    soup = BeautifulSoup(file)
    print(soup.prettify())




