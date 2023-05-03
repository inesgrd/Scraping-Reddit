from inspect import Attribute
import requests
import urllib.request
from bs4 import BeautifulSoup
import time
from pprint import pprint
from minet.scrape.std import get_display_text
import json

## Script that scrap from reddit the 7th first posts in one community the title, link, date, votes, comments, and texts; user not available

#choose the community; has to be written as it would be in the url
#stored in a json file

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
  text = post.select_one(".Chtkt3BCZQruf0LtmFg2c")
  if text is None:
    result1 = {
      "title": title,
      "link": link,
      "date": date,
      "votes": votes,
      "comments": comments
    }
    posts.append(result1)
  else:
    for i in text:
      para = i.select("._1qeIAgB0cPwnLhDF9XSiJM")
      para = get_display_text(para)
      result2 = {
        "title": title,
        "link": link,
        "date": date,
        "text": para,
        "votes": votes,
        "comments": comments
      }
      posts.append(result2)
tf = open("redditscrap_" + community + ".json", "w")
json.dump(posts, tf)
tf.close()


## Difficulties and questions ##

## Questions: 
#Vote : no other class to select, why? => json version to better get it
#Why not possible to have more than 7 at a time ? => json version to do that
#user not in the html, where to get it? => json version to do that


## TEST 6: to get the text attached to the post ##
# last working code but text not associted with the rest of the info from the psot

#for i in text:
#        if i is None:
#            print("Nothing")
#        else:
#            para = i.select("._1qeIAgB0cPwnLhDF9XSiJM")
#            para = get_display_text(para)
#            result = {
#              "text": para
#            }
#            posts.append(result)
#    result = {
#        "title": title,
#        "link": link,
#        "date": date,
#        "votes": votes,
#        "comments": comments
#    }
#    posts.append(result)
#tf = open("redditscrap_" + community + ".json", "w")
#json.dump(posts, tf)
#tf.close()


## TEST 5 : to get the text ## 
#do not print anything

#for post in allposts:
#    title = post.select_one('a[data-click-id="body"]').get_text()
#    link = post.select_one('a[data-click-id="body"]').get('href')
#    date = post.select_one('span[data-testid="post_timestamp"]').get_text()
#    votes = post.select_one("._1rZYMD_4xY3gRcSS3p8ODO").get_text()
#    comments = post.select_one('a[data-click-id="comments"]').get_text()
#    nbcom = comments.split()
#    nbcom.pop()
#    nbcom = ''.join(nbcom)
#    text = post.select(".Chtkt3BCZQruf0LtmFg2c")
#    for i in text:
#        if i is None:
#          result1 = {
#            "title": title,
#            "link": link,
#            "date": date,
#            "votes": votes,
#            "comments": comments
#          }
#          posts.append(result1)
#          pprint(posts)
#        else:
#            para = i.select("._1qeIAgB0cPwnLhDF9XSiJM")
#            para = get_display_text(para)
#            result2 = {
#              "title": title,
#              "link": link,
#              "date": date,
#              "text": para,
#              "votes": votes,
#              "comments": comments
#            }
#            posts.append(result2)
#            pprint(posts)
#pprint(posts)

## TEST 4 : trying to get text and the rest together ##

#text appears in another part in the json document ; it is next to the right information but not in the same pack
#if the text is put together with the rest, then when there is no text, no information is collected
#either have the text separated and have all or only have post with text
#for i in text:
#        if i is None:
#            print("Nothing")
#        else:
#            para = i.select("._1qeIAgB0cPwnLhDF9XSiJM")
#            para = get_display_text(para)
#            result = {
#              "title": title,
#              "link": link,
#              "text": para,
#              "date": date,
#              "votes": votes,
#              "comments": comments
#            }
#            posts.append(result)


## TEST 3 : trying to get user (nope) ##

##User : not in the html page !!!!!! 
#Not working in python for user 
#user = post.select_one('a[data-click-id="user"]')
#NOPE user = post.select_one("._2tbHP6ZydRpjI44J3syuqC  _23wugcdiaj44hdfugIAlnX oQctV4n0yUb0uiHDdGnmE")
#NOPE user user = post.select_one("a[data-click-id='user']")
#USER not in .Post why??? ; not possible 
#=> Ask Benjamin where to get it 


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