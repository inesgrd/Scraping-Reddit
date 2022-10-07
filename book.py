import requests
import urllib.request
from bs4 import BeautifulSoup
import time
from pprint import pprint

#Trying to get the text of a post 

mainurl = 'https://www.reddit.com/r/books/'
url = mainurl
headers = {'user-agent': 'ines'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
response.status_code

allposts = soup.select(".Post")

for post in allposts:
    text = post.select_one("._1qeIAgB0cPwnLhDF9XSiJM")
    pprint(text)

posts = []


## TEST 2 ##
#get some text but still have the <p class etc in it so not clean
#tried with the class of one paragraph to see if it coumd get the text but nope
#Not working .get_text() because some posts don't have a text and cannot do that on a empty result

#for post in allposts:
#    text = post.select_one("._1qeIAgB0cPwnLhDF9XSiJM")
#    posts.append(text) 
#    str(post)
#    pprint(posts)


## TEST 1 ##
#no generic class because it is in a div, 
#Not working text = post.select_one('div[data-adclicklocation="media"]')
#wroking by searching with the class ; 
#Not working .get_text()

#for post in allposts:
#    for post in allposts:
#    text = post.select_one(".Chtkt3BCZQruf0LtmFg2c")
#    pprint(text)


