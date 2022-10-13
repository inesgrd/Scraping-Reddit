from inspect import Attribute
import requests
import urllib.request
from bs4 import BeautifulSoup
import time
from pprint import pprint
from minet.scrape.std import get_display_text

## Fonction that scrap from reddit the 7th first posts in one community the title link date votes comments ; user not available

#choose the community; has to be written as it would be in the url


community = input("Choose a community on Reddit to scrap: ")

def recup_reddit(community):
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
    pprint(posts)
recup_reddit(community)