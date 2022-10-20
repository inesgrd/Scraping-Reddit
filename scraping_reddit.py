import json
import requests
import csv
import urllib.request
import time
from pprint import pprint
from datetime import datetime
import argparse

## FUSION + ARG

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

group.add_argument("-c", "--community", action="store_true", help="to scrape a community")
group.add_argument("-u", "--user", action="store_true", help="to scrape a user")
group.add_argument("-s", "--search", action="store_true", help="to scrape a search page")

parser.add_argument("--posts", action="store_true", help="to scrape the posts")
parser.add_argument("--coms", action="store_true", help="to scrape the comments")
parser.add_argument("--commu", action="store_true", help="to scrape the community in the result of a search")

parser.add_argument("name", help="either the name of the community OR the name of an user OR the keyword searched in Reddit")

args = parser.parse_args()

after = ''

if args.community:
    url = f'https://www.reddit.com/r/{args.name}/new.json?limit=100'
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
    with open("posts_"+args.name+"_scraping_reddit.csv.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=output_CSV_header)
        writer.writeheader()
        while True:
            url = f'https://www.reddit.com/r/{args.name}/new.json?limit=100{after}'
            headers = {'user-agent': 'r2d2'}
            response = requests.get(url + after, headers=headers)
            data = json.loads(response.text)
            children = data['data']['children']
            if args.posts:
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
            else:
                print("request in community not possible")

elif args.user:
    if args.posts:
        url = f'https://www.reddit.com/user/{args.name}/submitted.json?limit=100&sort=new'
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
        with open("posts_"+args.name+"_scraping_reddit.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=output_CSV_header)
            writer.writeheader()
            while True:
                url = f'https://www.reddit.com/user/{args.name}/submitted.json?limit=100{after}&sort=new'
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
    elif args.coms:
        url = f'https://www.reddit.com/user/{args.name}/comments.json?limit=100&sort=new'
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
        with open("comments_"+args.name+"_scraping_reddit.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=output_CSV_header)
            writer.writeheader()
            while True:
                url = f'https://www.reddit.com/user/{args.name}/comments.json?limit=100{after}&sort=new'
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
    else:
        print("request in user not possible")

elif args.search:
    if args.posts:
        url = f'https://www.reddit.com/search.json?limit=100&q={args.name}&sort=new'
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
        with open("search_posts_"+args.name+"_scraping_reddit.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=output_CSV_header)
            writer.writeheader()
            while True:
                    url = f'https://www.reddit.com/search.json?limit=100{after}&q={args.name}&sort=new'
                    headers = {'user-agent': 'r2d2'}
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
    elif args.commu:
        url = f'https://www.reddit.com/search.json?limit=100&q={args.name}&type=sr'
        output_CSV_header = [
            "subreddit",
            "subreddit_name",
            "subreddit_id",
            "subreddit_subscribers",
            "date_utc",
            "link_post",
            "description_subreddit",
            "rules_of_publication_subreddit"]
        with open("search_community_"+args.name+"_scraping_reddit.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=output_CSV_header)
            writer.writeheader()
            while True:
                url = f'https://www.reddit.com/search.json?limit=100{after}&q={args.name}&type=sr'
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
    else:
        print("request in search not possible")

else:
    print("global request not possible")
