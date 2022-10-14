import json
import requests
import csv
import urllib.request
import time
from pprint import pprint
from datetime import datetime

## AUTHOR COMMENTS 
#got many identical ones idkw
#Check the with open w/a ?


user = input("Choose a username on Reddit to scrap: ")

mailurl = 'https://www.reddit.com/r/'
after = ''
url = 'https://www.reddit.com/user/'+ user + '/comments.json?limit=100&sort=new'

name_header = [
    "subreddit",
    "subreddit_id",
    "title",
    "link_post",
    "date_utc",
    "text",
    "link_joined",
    "score",
    "comments",
    "awards"]

with open("com_"+user+"scraping_reddit.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=name_header)
    writer.writeheader()

    while True:
        url = url = 'https://www.reddit.com/user/'+ user + '/comments.json?limit=100' + after + '&sort=new'
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
                    "title": child['link_title'],
                    "link_post": 'https://www.reddit.com'+ child['permalink'],
                    "date_utc": date,
                    "text": child['body'],
                    "link_joined": child['link_url'],
                    "score": child['score'],
                    "comments": child['num_comments'],
                    "awards": child['total_awards_received']
                }
                posts.append(result)
            
                writer.writerows(posts)

        if data['data']['after']:
            after = "&after=" + data['data']['after']
        else:
            break


## Author's comments
#select an author -> need info 

#karma? not in the j.son format :( => how to get it 

#url.json changes /r in /user
#'https://www.reddit.com/user/'+ user + '/comments.json?limit=100' + 'after' + &sort=new


#got rid of author + subreddit_subscribers + domain
#link_title = title of the post the author made or commented
#body = (first) comment/text
#link_url = link of the publication

#Attention : got multiple times the same comments 

#karma? not in the j.son format :( => how to get it 