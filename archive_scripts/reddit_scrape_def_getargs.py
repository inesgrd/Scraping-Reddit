from fileinput import filename
import json
import requests
import csv
from datetime import datetime
import argparse

## FUSION + ARG (not in def) + DEF + MODULO CODE

def get_args():
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

    community = args.community
    user = args.user
    search = args.search
    posts = args.posts
    coms = args.coms
    commu = args.commu
    name = args.name

    return community, user, search, posts, coms, commu, name

def build_url(name, community, user, posts, coms, search, commu, after):
    reddit_url = 'https://www.reddit.com'
    f_json = '.json?limit=100' 
    if community:     
        path = 'r'        
        page = 'new'
        url_first = f'{reddit_url}/{path}/{name}/{page}{f_json}{after}'        
    elif user:        
        path = 'user'
        sort = '&sort=new'      
        if posts:     
            page = 'submitted'
        elif coms:    
            page = 'comments'
        url_first = f'{reddit_url}/{path}/{name}/{page}{f_json}{after}{sort}'
    elif search:
        path = 'search'
        if posts:
            sort = '&sort=new'
        elif commu:
            sort = '&type=sr'
        url_first = f'{reddit_url}/{path}{f_json}{after}&q={name}{sort}'
    return url_first

def output_csv(posts, user, coms, commu):
    output_base = [
        "subreddit",
        "subreddit_id",
        "link_post",
        "date_utc",
    ]
    if posts:
        output_spe = [
            "subreddit_subscribers",
            "title_post",
            "text_post",
            "link_joined",
            "score_post",
            "comments_post",
            "awards_post",
            "domain_link_joined"
        ]
        if not user:
            output_spe = output_spe + [
                "author_post"
            ]
    elif coms:
            output_spe = [
                "title_post",
                "author_post",
                "text_com",
                "link_joined",
                "score_com",
                "comments_post",
                "awards_com"
            ]
    elif commu:
        output_spe = [
            "subreddit_name",
            "subreddit_subscribers",
            "description_subreddit",
            "rules_of_publication_subreddit"
        ]
    output_CSV_header = output_base + output_spe
    return output_CSV_header

def name_csv(name, community, user, posts, coms, search, commu):
    if community:
        file_name_CSV = f'community_posts_{name}_scraping_reddit.csv'
    elif user:
        if posts:
            file_name_CSV = f'user_posts_{name}_scraping_reddit.csv'
        elif coms:
            file_name_CSV = f'user_comments_{name}_scraping_reddit.csv'
    elif search:
        if posts :
            file_name_CSV = f'search_posts_{name}_scraping_reddit.csv'
        elif commu:
            file_name_CSV = f'search_commu_{name}_scraping_reddit.csv'
    return file_name_CSV

#If with open() is a function, the if __name__ == "__main__":, at the end do not recognise stuff in it
def create_file_CSV(file_name_CSV, output_CSV_header):
    with open(file_name_CSV, "w") as f :
        writer = csv.DictWriter(f, fieldnames=output_CSV_header)
        writer.writeheader()

        def data_url(url_first): #without the after !!!!!
            url_first = build_url(name)
            headers = {'user-agent': 'r2d2'}
            response = requests.get(url, headers=headers)
            data_first = json.loads(response.text)
            return data_first

        def data_children(data):
            children_first = data['data']['children']
            return children_first

        def data_posts(children_first):
            for child in children_first:
                child = child['data']
                result = {
                    "date_utc": datetime.utcfromtimestamp(int(child['created_utc'])).isoformat()
                }
                if posts:
                    result["subreddit"] = child["subreddit"]
                    result["subreddit_id"] = child["subreddit_id"]
                    result["subreddit_subscribers"] = child["subreddit_subscribers"]
                    result["title_post"] = child["title"]
                    result["link_post"] = 'https://www.reddit.com{permalink}'.format(permalink = child["permalink"])
                    result["text_post"] = child["selftext"]
                    result["link_joined"] = child["url"]
                    result["score_post"] = child["score"]
                    result["comments_post"] = child["num_comments"]
                    result["awards_post"] = child["total_awards_received"]
                    result["domain_link_joined"] = child["domain"]
                    if not user:
                        result["author_post"] = child['author']
                elif coms:
                    result["subreddit"] = child["subreddit"]
                    result["subreddit_id"] = child["subreddit_id"]
                    result["title_post"] = child["link_title"]
                    result["link_post"] = 'https://www.reddit.com{permalink}'.format(permalink = child["permalink"])
                    result["author_post"] = child["link_author"]
                    result["text_com"] = child["body"]
                    result["link_joined"] = child["link_url"]
                    result["score_com"] = child["score"]
                    result["comments_post"] = child["num_comments"]
                    result["awards_com"] = child["total_awards_received"]
                elif commu:
                    result["subreddit"] = child["display_name"]
                    result["subreddit_name"] = child["title"]
                    result["subreddit_id"] = child["name"]
                    result["subreddit_subscribers"] = child["subscribers"]
                    result["link_post"] = 'https://www.reddit.com{permalink}'.format(permalink = child["url"])
                    result["description_subreddit"] = child["public_description"]
                    result["rules_of_publication_subreddit"] = child["submit_text"]
            return result 

        writer.writerow(result)

        while True:
            def build_url(name, after):
                reddit_url = 'https://www.reddit.com'
                f_json = '.json?limit=100'
                after = "&after=" + data['data']['after'] 
                if community:     
                    path = 'r'        
                    page = 'new'
                    url = f'{reddit_url}/{path}/{name}/{page}{f_json}{after}'        
                elif user:        
                    path = 'user'
                    sort = '&sort=new'      
                    if posts:     
                        page = 'submitted'
                    elif coms:    
                        page = 'comments'
                    url = f'{reddit_url}/{path}/{name}/{page}{f_json}{after}{sort}'
                elif search:
                    path = 'search'
                    if posts:
                        sort = '&sort=new'
                    elif commu:
                        sort = '&type=sr'
                    url = f'{reddit_url}/{path}{f_json}{after}&q={name}{sort}'
                return url
            
            data = data_url(url) #url not recognized here if with open() is not a function
            children = data_children(data)
            result = data_posts(children)
            writer.writerow(result)

            if data['data']['after']:
                after = "&after=" + data['data']['after'] #after underlined wierd if with open() 
            else:
                break

    return writer.writerow(result)

if __name__ == "__main__": #all recoginzed if with open() is not a function + do understand that ?boilerplate?
    community, user, search, posts, coms, commu, name = get_args()
    url = build_url(name, community, user, posts, coms, search, commu) #add after in the function ?
    output_CSV_header = output_csv(name, user, posts, coms, commu)
    file_name_CSV = name_csv(name, community, user, posts, coms, search, commu)
    data_first = data_url(url_first) #data_url not recognized when with open() is a function
    children_first = data_children(data_first) #data_children not recognized when with open() is a function
    result_first = data_posts(children_first) #data_posts not recognized when with open() is a function
    url = build_url(name, after, community, user, posts, coms, search, commu) #after not recognized when with open() is a function
    data = data_url(url) #data_url not recognized when with open() is a function
    children = data_children(data) #data_children not recognized when with open() is a function
    result = data_posts(children) #data_posts not recognized when with open() is a function
    



            

### TO DO :
#Kelly's comments 
# def get_args() 
# if __name__ == "__main__":
#    community, user, search, posts, coms, commu, name = get_args()
#    ......
#first time and fonction outside While (after = '')
#in While to call all the function
#Beatrice : do a function that calls all the function?



#def build_url(args, after=""):
# ....
# return f'https://www.reddit.com/{path}/{args.name}/{page}.json?limit=100{after}'
# puis build_url(args) pour la première url, et build_url(args, after) après


## TEST 1 : function for url 

# def build_url(args):
#     reddit_url = 'https://www.reddit.com/'
#     f_json = '.json?limit=100'
#     if args.community:
#         url = f'{reddit_url}r/{args.name}/new{f_json}'
#     elif args.user:
#         if args.posts:
#             url = f'{reddit_url}user/{args.name}/submitted{f_json}&sort=new'
#             print (url)
#         elif args.coms:
#             url = f'{reddit_url}user/{args.name}/comments{f_json}&sort=new'
#     elif args.search:
#         if args.posts:
#             url = f'{reddit_url}search{f_json}&q={args.name}&sort=new'
#         elif args.commu: 
#             url = f'{reddit_url}search{f_json}&q={args.name}&type=sr'
#     return url





