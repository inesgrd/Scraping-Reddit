import json
import requests
import csv
import urllib.request
import time
from pprint import pprint
from datetime import datetime

## AUTHOR POSTS
#got many identical ones idkw
#Check the with open w/a ?

user = input("Choose a username on Reddit to scrap: ")

mailurl = 'https://www.reddit.com/r/'
after = ''
url = 'https://www.reddit.com/user/'+ user + '/submitted.json?limit=100&sort=new'

name_header = [
    "subreddit",
    "subreddit_id",
    "subreddit_subscribers",
    "title",
    "link_post",
    "date_utc",
    "text",
    "link_joined",
    "score",
    "comments",
    "awards",
    "domain"]

with open("posts_"+user+"scraping_reddit.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=name_header)
    writer.writeheader()

    while True:
        url = 'https://www.reddit.com/user/'+ user + '/submitted.json?limit=100' + after + '&sort=new'
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



## Author's posts
#select an author -> need info 


#got rid of author

#url.json changes /r in /user
#url dans la boucle
#'https://www.reddit.com/user/' + user +'/submitted.json?limit=100' + 'after' + &sort=new

#changes the name of the doc

#karma? not in the j.son format :( => how to get it 




