
import requests
import urllib.request
from bs4 import BeautifulSoup
import time
from pprint import pprint

#Fonction qui récupère les posts dans une communauté reddit ; exemple avec r/space 

space = 'https://www.reddit.com/r/space/'

url = space
headers = {'user-agent': 'ines'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
response.status_code

allposts = soup.select(".Post")

posts = []
for post in allposts:
    title = post.select_one("._eYtD2XCVieq6emjKBH3m").get_text()
    date = post.select_one("._2VF2J19pUIMSLJFky-7PEI").get_text()
    votes = post.select_one("._1rZYMD_4xY3gRcSS3p8ODO").get_text()
    comments = post.select_one(".FHCV02u6Cp2zYL0fhQPsO").get_text()
    result = {
        "title": title,
        "date": date,
        "votes": votes,
        "comments": comments
    }
    posts.append(result)
pprint(posts)


#("a[data-click-id='user']").href

#LIGNE  a = post.select(".SQnoC3ObvgnGjWt90zD9Z")
    #link = a.select('a[href]')
    #print(link)
#NOPE author = post.select_one("._2tbHP6ZydRpjI44J3syuqC  _23wugcdiaj44hdfugIAlnX oQctV4n0yUb0uiHDdGnmE")


#for post in allposts:
#    title = post.select_one("._eYtD2XCVieq6emjKBH3m").get_text()
#    link = 
#    author = 
#    date = post.select_one("._2VF2J19pUIMSLJFky-7PEI").get_text()
#    votes = post.select_one("._1rZYMD_4xY3gRcSS3p8ODO").get_text()
#    comments = post.select_one(".FHCV02u6Cp2zYL0fhQPsO").get_text()  
#    result = {
#        "title": title,
#        "link": link,
#        "author": author,
#        "date": date,
#        "votes": votes,
#        "comments": comments
#    }
#    posts.append(result)
#pprint(posts)




#for post in allposts:
    #tittle = post.select_one("._eYtD2XCVieq6emjKBH3m")
    #print(tittle.get_text())


#for post in allposts:
    #t = soup.select("body h3")
    #print(t)



## TEST ##

#tittle = soup.find('h3', {'class': '_eYtD2XCVieq6emjKBH3m'})
#print(tittle)

#ti = soup.select("._eYtD2XCVieq6emjKBH3m")
#print(ti)

#t = soup.find_all("._eYtD2XCVieq6emjKBH3m")
#print(t)
#len(t)


#body = soup.select(id='2x-container')

#post = soup.select('div', {'class': 'Post'})

#post entier : _1poyrkZ7g36PawDueRza-J _11R7M_VOgKO1RJyRSRErT3 
#contien post 

#[attribute*="value"]
#post = soup.select('.rpBJOHq2PR60pnwJlUyP0')

#recup tous les posts
#allpost = soup.select(".scrollerItem")
#print(len(allpost))
#for post in allpost:
#    print(post.contents)
#print("TEST", allpost, "TEST2")

#tittlepost = allpost.select('h3*')


#titlepost = items.find('h3', {'class': '_eYtD2XCVieq6emjKBH3m'})

#utiliser seclect pour trouver un css à la place de find pour trouver avec un sélecteur
#/h3[@class='_eYtD2XCVieq6emjKBH3m']