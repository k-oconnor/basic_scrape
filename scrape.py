# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# author - Kevin O'Connor


from bs4 import BeautifulSoup
import pandas
import time
import urllib


main_url = "http://books.toscrape.com/index.html"

import requests
result = requests.get(main_url)
print (result.text[:1000])

from bs4 import BeautifulSoup
soup = BeautifulSoup(result.text, 'html.parser')
print(soup.prettify()[:1000])

def getAndParseURL(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return(soup)

a = soup.find("article", class_ = "product_pod").div.a.get('href')
print(a)

titles = main_page_product_urls = [x.div.a.get('href') for x in soup.findAll("article", class_= "product_pod")]
print(str(len(main_page_product_urls))+ "fetched products URLs")
print(titles)

def getBooksURLs(url):
    soup = getAndParseURL(url)
    return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.findAll("article", class_ = "product_pod")])

import re
page_urls = [main_url]
soup = getAndParseURL(page_urls[0])
while len(soup.findAll("a", href=re.compile("page"))) ==2 or len(page_urls)==1:
    
    new_url = "/".join(page_urls[-1].split("/")[:-1]) + "/" + soup.findAll("a", href=re.compile("page"))[-1].get("href")
    page_urls.append(new_url)
    soup = getAndParseURL(new_url)

print(str(len(page_urls)) + "fetched URLs")

booksURLs = []
for page in page_urls:
    booksURLs.extend(getBooksURLs(page))

print(str(len(booksURLs)) + "fetched URLs")

title=[] #List to store name of the product
price=[] #List to store price of the product
stock_amount=[] #List amount of books in stock
rating=[] #Ratings for each book
genre = [] # Each book's genre

for url in booksURLs:
    soup = getAndParseURL(url)
    # Book Title
    title.append(soup.find("div", class_ = re.compile("product_main")).h1.text)
    # Product Price
    price.append(soup.find("p", class_= "price_color").text[2:])
    # Number of each book availabile in stock
    stock_amount.append(re.sub("[^0-9]", "", soup.find("p", class_ = "instock availability").text))
    # Book rating (1-5)
    rating.append(soup.find("p", class_ = re.compile("star-rating")).get("class")[1])
    # book genre/category
    genre.append(soup.find("a", href = re.compile("../category/books/")).get("href").split("/")[3])
    
# Push data into pandas
scrape_data = pandas.DataFrame({'title': title, 'price':price, 'stock_amount':stock_amount, 'rating':rating, 'genre':genre })
scrape_data.head()






