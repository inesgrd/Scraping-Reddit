import json
import requests
import csv
import urllib.request
import time
from pprint import pprint
from datetime import datetime

## AUTHOR POSTS

user = input("Choose a username on Reddit to scrap: ")

after = ''
url = f'https://www.reddit.com/user/{user}/submitted.json?limit=100&sort=new'

output_CSV_header = [
    "subreddit",
    "subreddit_id",
    "subreddit_subscribers",
    "title_post",
    "link_post",
    "date_utc",
    "text_post",
    "link_joined",
    "score_post",
    "comments_post",
    "awards_post",
    "domain_link_joined"]

with open("posts_"+user+"_scraping_reddit.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=output_CSV_header)
    writer.writeheader()

    while True:
        url = f'https://www.reddit.com/user/{user}/submitted.json?limit=100{after}&sort=new'
        headers = {'user-agent': 'r2d2'}
        response = requests.get(url + after, headers=headers)
        data = json.loads(response.text)
        
        children = data['data']['children']
    
        for child in children:
            child = child['data']
            result = {
                "subreddit": child['subreddit'],
                "subreddit_id": child['subreddit_id'],
                "subreddit_subscribers": child['subreddit_subscribers'],
                "title_post": child['title'],
                "link_post": 'https://www.reddit.com{permalink}'.format(permalink = child["permalink"]),
                "date_utc": datetime.utcfromtimestamp(int(child['created_utc'])).isoformat(),
                "text_post": child['selftext'],
                "link_joined": child['url'],
                "score_post": child['score'],
                "comments_post": child['num_comments'],
                "awards_post": child['total_awards_received'],
                "domain_link_joined": child['domain']
            }
            writer.writerow(result)

        if data['data']['after']:
            after = "&after=" + data['data']['after']
        else:
            break



## Author's posts

#select an author -> need info 
#karma? not in the j.son format :( => how to get it