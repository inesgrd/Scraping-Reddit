import json
import requests
import csv
import urllib.request
import time
from pprint import pprint
from datetime import datetime

## COMMUNITY POSTS
#got many identical ones idkw
#Check the with open w/a ?


community = input("Choose a community on Reddit to scrap: ")

mailurl = 'https://www.reddit.com/r/'
after = ''
url = 'https://www.reddit.com/r/'+community+'/new.json?limit=100'

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

with open("scraping_reddit_"+community+".csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=name_header)
    writer.writeheader()

    while True:
        url = url+after
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


## To fix :
#the url format

#urljoin check python
#"lemonde.fr?key1=" + var1 + '&key2=' + var2
#"lemonde.fr?key1={var1}&key2={var2}".format(var1=var1)


## Notes for developping this script : ##

#argparse library 
#sys library
#click library 


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


# Space : 51062
#Terminal <scraping_reddit_space.csv cut -f4 -d',' | sort -u | wc -l
# >>> 825
#only 825 posts ?? 


