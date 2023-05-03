import json
import requests
import csv
import urllib.request
import time
from pprint import pprint
from datetime import datetime

## AUTHOR COMMENTS 

user = input("Choose a username on Reddit to scrap: ")

after = ''
url = f'https://www.reddit.com/user/{user}/comments.json?limit=100&sort=new'

output_CSV_header = [
    "subreddit",
    "subreddit_id",
    "title_post",
    "link_post",
    "date_utc",
    "text_com",
    "link_joined",
    "score_com",
    "comments_post",
    "awards_com"]

with open("comments_"+user+"_scraping_reddit.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=output_CSV_header)
    writer.writeheader()

    while True:
        url = f'https://www.reddit.com/user/{user}/comments.json?limit=100{after}&sort=new'
        headers = {'user-agent': 'r2d2'}
        response = requests.get(url + after, headers=headers)
        data = json.loads(response.text)
        
        children = data['data']['children']
    
        for child in children:
            child = child['data']
            result = {
                "subreddit": child['subreddit'],
                "subreddit_id": child['subreddit_id'],
                "title_post": child['link_title'],
                "link_post": 'https://www.reddit.com{permalink}'.format(permalink = child["permalink"]),
                "date_utc": datetime.utcfromtimestamp(int(child['created_utc'])).isoformat(),
                "text_com": child['body'],
                "link_joined": child['link_url'],
                "score_com": child['score'],
                "comments_post": child['num_comments'],
                "awards_com": child['total_awards_received']
            }
            writer.writerow(result)

        if data['data']['after']:
            after = "&after=" + data['data']['after']
        else:
            break


## Author's comments

#select an author -> need info 
#karma? not in the j.son format :( => how to get it