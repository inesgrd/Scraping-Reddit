import requests
import urllib.request
from bs4 import BeautifulSoup
import time

#Fonction qui récupère les posts dans une communauté reddit ; exemple avec r/space 

space = 'https://www.reddit.com/r/space/'

url = space
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
soup

body = soup.find(id='2x-container')
body

items = body.find_all('div')
items
#len(items)
#print(type(items)) : <class 'bs4.element.ResultSet'>

titlepost = items.find('h3', {'class': '_eYtD2XCVieq6emjKBH3m'})
print(titlepost)