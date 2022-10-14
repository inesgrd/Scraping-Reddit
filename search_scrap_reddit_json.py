import json
import requests
import csv
import urllib.request
import time
from pprint import pprint
from datetime import datetime

## SEARCH POSTS
#got many identical ones idkw
#Check the with open w/a ?

keyword = input("Choose a keyword on Reddit to scrap: ")

mailurl = 'https://www.reddit.com/r/'
after = ''
url = 'https://www.reddit.com/search.json?limit=100&q=' + keyword + '&sort=new'

name_header = [
    "subreddit",
    "subreddit_id",
    "subreddit_subscribers",
    "title",
    "link_post",
    "author",
    "date_utc",
    "text",
    "link_joined",
    "score",
    "comments",
    "awards",
    "domain"]

with open("search_posts_"+keyword+"_scraping_reddit.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=name_header)
    writer.writeheader()

    while True:
        url = 'https://www.reddit.com/search.json?limit=100' + after + '&q=' + keyword + '&sort=new'
        headers = {'user-agent': 'r2d2'}
        response = requests.get(url + after, headers=headers)
        data = json.loads(response.text)
        
        children = data['data']['children']
        posts = []

        for child in children:
                child = child['data']
                date_utc = child['created_utc']
                ts = int(date_utc)
                date = datetime.utcfromtimestamp(ts).isoformat()
                result = {
                    "subreddit": child['subreddit'],
                    "subreddit_id": child['subreddit_id'],
                    "subreddit_subscribers": child['subreddit_subscribers'],
                    "title": child['title'],
                    "link_post": 'https://www.reddit.com'+ child['permalink'],
                    "author": child['author'],
                    "date_utc": date,
                    "text": child['selftext'],
                    "link_joined": child['url'],
                    "score": child['score'],
                    "comments": child['num_comments'],
                    "awards": child['total_awards_received'],
                    "domain": child['domain']
                }
                posts.append(result)
            
                writer.writerows(posts)

        if data['data']['after']:
            after = "&after=" + data['data']['after']
        else:
            break


## POSTS search 

#Add a limit

#Publication : ok
#Comments : does not work, still give the publication page info
#Community : works, keyword related to the community (idk how it does that when not mentionned in the name nor the description)
#User : get some users but not the same between reddit search and the .json one 
