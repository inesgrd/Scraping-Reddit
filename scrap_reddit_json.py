import json
import requests
import csv
import urllib.request
import time
from pprint import pprint
from datetime import datetime


## Scrap Reddit from json 

boucle = True
after = ''
url = 'https://www.reddit.com/r/space/hot.json?limit=100'

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

with open("reddit_scrape_space_hot.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=name_header)
    writer.writeheader()

    while boucle:
        url = url+after
        headers = {'user-agent': 'r2d2'}
        response = requests.get(url + after, headers=headers)
        data = json.loads(response.text)
        
        children = data['data']['children']
        posts = []
        
        for child in children:
            subreddit = child['data']['subreddit']
            subreddit_id = child['data']['subreddit_id']
            subreddit_subscribers = child['data']['subreddit_subscribers']
            title = child['data']['title']
            link_post = child['data']['permalink']
            author = child['data']['author']
            date_utc = child['data']['created_utc']
            ts = int(date_utc)
            date = datetime.utcfromtimestamp(ts).isoformat()
            text = child['data']['selftext']
            link_joined = child['data']['url']
            score = child['data']['score']
            comments = child['data']['num_comments']
            awards = child['data']['total_awards_received']
            domain = child['data']['domain']
            result = {
                "subreddit": subreddit,
                "subreddit_id": subreddit_id,
                "subreddit_subscribers": subreddit_subscribers,
                "title": title,
                "link_post": link_post,
                "author": author,
                "date_utc": date,
                "text": text,
                "link_joined":link_joined,
                "score": score,
                "comments": comments,
                "awards": awards,
                "domain": domain
            }
            posts.append(result)
        
            writer.writerows(posts)

        if data['data']['after']:
            after = "&after=" + data['data']['after']
            boucle = True
        else:
            boucle = False



## what is it ? 

#thumbnail ; picture in a post, get it ?
#wls ; what is that 
#previw image ; take it ?

