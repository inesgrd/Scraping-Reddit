import json
import requests
import csv
import urllib.request
import time
from pprint import pprint
from datetime import datetime

## COMMUNITY POSTS

community = input("Choose a community on Reddit to scrap: ")

after = ''
url = f'https://www.reddit.com/r/{community}/new.json?limit=100'

output_CSV_header = [
    "subreddit",
    "subreddit_id",
    "subreddit_subscribers",
    "title_post",
    "link_post",
    "author_post",
    "date_utc",
    "text_post",
    "link_joined",
    "score_post",
    "comments_post",
    "awards_post",
    "domain_link_joined"]

with open("posts_"+community+"_scraping_reddit.csv.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=output_CSV_header)
    writer.writeheader()

    while True:
        url = f'https://www.reddit.com/r/{community}/new.json?limit=100{after}'
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
                "author_post": child['author'],
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




## Notes for developping this script : ##


## Community 
#select a community 
# option : selection 1 or 2 or 3 keywords contained in posts in this community 

#Scraping a all the posts from a community starting with the most recent one
#'https://www.reddit.com/r/' + community + '/new.json?limit=100' + 'after'

#Scraping all the posts from a community that contains one keyword stating with the most recent one 
#'https://www.reddit.com/r/' + community + '/search.json?limit=100' + 'after' + '&q='+ keyword + '&restrict_sr=1&sr_nsfw=&sort=new'

#Scraping all the posts from a community that contains 2 keywords stating with the most recent one 
#'https://www.reddit.com/r/' + community + '/search.json?limit=100' + 'after' + '&q='+ keyword1 + '%20'+ keyword2 + '&restrict_sr=1&sr_nsfw=&sort=new'

#Scraping all the posts from a community that contains 2 keywords stating with the most recent one 
#'https://www.reddit.com/r/' + community + '/search.json?limit=100' + 'after' + '&q='+ keyword1 + '%20'+ keyword2 + '%20'+ keyword3 +'&restrict_sr=1&sr_nsfw=&sort=new'