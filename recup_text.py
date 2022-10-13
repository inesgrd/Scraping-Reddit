from inspect import Attribute
import requests
import urllib.request
from bs4 import BeautifulSoup
import time
from pprint import pprint
from minet.scrape.std import get_display_text

## Script that get the text from the first 7th Post of Reddit (BeautifulSoup)

#choose the community; has to be written as it would be in the url
#Attention ; only get the text displayed on the page (if there is text in a post but cannot see it in the page, it's not collected)

community = input("Choose a community on Reddit to scrap: ")

mainurl = 'https://www.reddit.com/r/'
url = mainurl+community
headers = {'user-agent': 'ines'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
response.status_code

allposts = soup.select(".Post")

posts = []

for post in allposts:
    text = post.select(".Chtkt3BCZQruf0LtmFg2c")
    for i in text:
        if i is None:
            print("Nothing")
        else:
            para = i.select("._1qeIAgB0cPwnLhDF9XSiJM")
            para = get_display_text(para)
            result = {
                "text": para
            }
            posts.append(result)
pprint(posts)



## TEST 4 ##
#install Minet avec pip
#use 
#text = post.select(".Chtkt3BCZQruf0LtmFg2c")
#    for i in text:
#        if i is None:
#            print("Nothing")
#        else:
#            para = i.select("._1qeIAgB0cPwnLhDF9XSiJM")
#            para = get_display_text(para)

## TEST 3 ##
#tried to apply the selection only if the result was not null ; got rid of the None problem
#worked but have one para for one element so don't know which para are together
#for post in allposts:
#    text = post.select(".Chtkt3BCZQruf0LtmFg2c")
#    for i in text:
#        if i is None:
#            pprint("Nothing")
#        else:
#            para = i.select("._1qeIAgB0cPwnLhDF9XSiJM")
#            pprint(para)


## TEST 2 ##
#get some text but still have the <p class etc in it so not clean
#only get the first paragraph of the text
#tried with the class of one paragraph to see if it could get the text but nope
#Not working .get_text() because some posts don't have a text and cannot do that on a empty result
#got None problem

#for post in allposts:
#    text = post.select_one("._1qeIAgB0cPwnLhDF9XSiJM")
#    posts.append(text) 
#    str(post)
#    pprint(posts)


## TEST 1 ##
#no generic class because it is in a div, 
#Not working text = post.select_one('div[data-adclicklocation="media"]')
#working by searching with the class ; 
#Not working .get_text()

#for post in allposts:
#    text = post.select_one(".Chtkt3BCZQruf0LtmFg2c")
#    pprint(text)



