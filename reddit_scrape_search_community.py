import json
import requests
import csv
import urllib.request
import time
from pprint import pprint
from datetime import datetime

## SEARCH COMMUNITY

keyword = input("Choose a keyword on Reddit to scrap: ")

after = ''
url = f'https://www.reddit.com/search.json?limit=100&q={keyword}&type=sr'

output_CSV_header = [
    "subreddit",
    "subreddit_name",
    "subreddit_id",
    "subreddit_subscribers",
    "date_utc",
    "link_post",
    "description_subreddit",
    "rules_of_publication_subreddit"]

with open("search_community_"+keyword+"_scraping_reddit.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=output_CSV_header)
    writer.writeheader()

    while True:
        url = f'https://www.reddit.com/search.json?limit=100{after}&q={keyword}&type=sr'
        headers = {'user-agent': 'r2d2'}
        response = requests.get(url + after, headers=headers)
        data = json.loads(response.text)
        
        children = data['data']['children']

        for child in children:
            child = child['data']
            result = {
                "subreddit": child['display_name'],
                "subreddit_name": child['title'],
                "subreddit_id": child['name'],
                "subreddit_subscribers": child['subscribers'],
                "date_utc": datetime.utcfromtimestamp(int(child['created_utc'])).isoformat(),
                "link_post": 'https://www.reddit.com{permalink}'.format(permalink = child["url"]),
                "description_subreddit": child['public_description'],
                "rules_of_publication_subreddit": child['submit_text']
            }          
            writer.writerow(result)

        if data['data']['after']:
            after = "&after=" + data['data']['after']
        else:
            break


## Reddit search 

#TO DO : 
#Add a limit

#Publication : ok
#Comments : does not work, still give the publication page info
#Community : works, keyword related to the community (idk how it does that when not mentionned in the name nor the description)
#User : get some users but not the same between reddit search and the .json one 