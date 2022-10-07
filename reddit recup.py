import requests
import urllib.request
from bs4 import BeautifulSoup
import time
from pprint import pprint
import json

#Fonction qui récupère les posts dans une communauté reddit ; exemple avec r/space 

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
  title = post.select_one('a[data-click-id="body"]').get_text()
  link = post.select_one('a[data-click-id="body"]').get('href')
  date = post.select_one('span[data-testid="post_timestamp"]').get_text()
  votes = post.select_one("._1rZYMD_4xY3gRcSS3p8ODO").get_text()
  comments = post.select_one('a[data-click-id="comments"]').get_text()
  nbcom = comments.split()
  nbcom.pop()
  nbcom = ''.join(nbcom)
  result = {
    "title": title,
    "link": link,
    "date": date,
    "votes": votes,
    "comments": comments
  }
  posts.append(result)
tf = open("redditscrap_" + community + ".json", "w")
json.dump(posts, tf)
tf.close()


## Difficulties and questions ##

##User : not in the html page !!!!!! 
#Not working in python for user 
#user = post.select_one('a[data-click-id="user"]')
#NOPE user = post.select_one("._2tbHP6ZydRpjI44J3syuqC  _23wugcdiaj44hdfugIAlnX oQctV4n0yUb0uiHDdGnmE")
#NOPE user user = post.select_one("a[data-click-id='user']")
#USER not in .Post why??? ; not possible 
#=> Ask Benjamin where to get it 

#Vote : no other class to select

#Why not possible to have more than 7 at a time ?

## TEST 2 : Working with other class that should not change ##

#other class used that should not change
#got rid of the word "commentaires" to only have the number
#not found for votes, no other class available

#posts = []
#for post in allposts:
#    title = post.select_one('a[data-click-id="body"]').get_text()
#    link = post.select_one('a[data-click-id="body"]').get('href')
#    date = post.select_one('span[data-testid="post_timestamp"]').get_text()
#    votes = post.select_one("._1rZYMD_4xY3gRcSS3p8ODO").get_text()
#    comments = post.select_one('a[data-click-id="comments"]').get_text()
#    nbcom = comments.split()
#    nbcom.pop()
#    nbcom = ''.join(nbcom)
#    result = {
#        "title": title,
#        "link": link,
#        "date": date,
#        "votes": votes,
#        "comments": comments
#    }
#   posts.append(result)
#pprint(posts)


## TEST 1 : Working but not optimal for all pages ##

#It works on other pages ! see if in a few days it is still)

#posts = []
#for post in allposts:
#    title = post.select_one("._eYtD2XCVieq6emjKBH3m").get_text()
#    link = post.select_one('a[data-click-id="body"]').get('href')
#    date = post.select_one("._2VF2J19pUIMSLJFky-7PEI").get_text()
#    votes = post.select_one("._1rZYMD_4xY3gRcSS3p8ODO").get_text()
#    comments = post.select_one(".FHCV02u6Cp2zYL0fhQPsO").get_text()
#    result = {
#        "title": title,
#        "link": link,
#        "date": date,
#        "votes": votes,
#        "comments": comments
#    }
#   posts.append(result)
#pprint(posts)