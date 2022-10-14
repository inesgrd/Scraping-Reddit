import json
import requests
import csv
import urllib.request
import time
from pprint import pprint
from datetime import datetime

## SEARCH COMMUNITY
#got many identical ones idkw
#Check the with open w/a ?

keyword = input("Choose a keyword on Reddit to scrap: ")

mailurl = 'https://www.reddit.com/r/'
after = ''
url = 'https://www.reddit.com/search.json?limit=100' + after + '&q=' + keyword + '&type=sr'

name_header = [
    "subreddit",
    "name",
    "subreddit_id",
    "subreddit_subscribers",
    "date_utc",
    "link_post",
    "description",
    "rules of publication"]

with open("search_commu_"+keyword+"_scraping_reddit.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=name_header)
    writer.writeheader()

    while True:
        url = 'https://www.reddit.com/search.json?limit=100' + after + '&q=' + keyword + '&type=sr'
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
                    "subreddit": child['display_name'],
                    "name": child['title'],
                    "subreddit_id": child['name'],
                    "subreddit_subscribers": child['subscribers'],
                    "date_utc": date,
                    "link_post": 'https://www.reddit.com'+ child['url'],
                    "description": child['public_description'],
                    "rules of publication": child['submit_text']
                }
                posts.append(result)
            
                writer.writerows(posts)

        if data['data']['after']:
            after = "&after=" + data['data']['after']
        else:
            break



## Reddit search 

#Add a limit

#Publication : ok
#Comments : does not work, still give the publication page info
#Community : works, keyword related to the community (idk how it does that when not mentionned in the name nor the description)
#User : get some users but not the same between reddit search and the .json one 

