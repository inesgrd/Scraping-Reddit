from fileinput import filename
import sys
import json
import requests
import csv
import urllib.request
import time
from pprint import pprint
from datetime import datetime
import argparse


# ------------------------------------------------#
# PARSE THE ARGUMENTS PASSED FROM THE COMMAND LINE
# ------------------------------------------------#
def get_args():
    """
    Parse the arguments passed from the command line and return
    their values in the form of meaningful variables.

    Return:
        community (str) : community page to scrape (indicates it is a community page to scrape)
        user (str) : user page to scrape (indicates it is a user page to scrape)
        search (str) : search function to scrape (indicates it is the search function to scrape)
        posts (str) : posts to scrape (indicates these are posts to scrape)
        coms (str) : comments to scrape (indicates these are comments to scrape)
        commu (str) : communities to scrape (indicates these are communities to scrape)
        name (str) : name of a community OR a user OR a keyword for a query 
    """
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


# ------------------------------------------------#
# CONCATENATE A URL TO SCRAPE
# ------------------------------------------------#
def build_url(name, community, user, posts, coms, search, commu, after=""): 
    """
    Using the command line arguments, concatenate the URL needed to access
    the Reddit page(s) that the user wants to scrape.

    Args:
        name (str) : name of a community OR name of a user OR a keyword for a query 
        user (str) : user page to scrape
        search (str) : search function to scrape 
        posts (str) : posts to scrape
        coms (str) : comments to scrape
        commu (str) : communities to scrape
        ## after (str) : id of the next json page OR null/void here

    Return:
        url_first (str) : URL to be requested and scraped
    """
    reddit_url = 'https://www.reddit.com'
    f_json = '.json?limit=100'
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
    print(f"calling {url}", file=sys.stderr)
    return url


# ------------------------------------------------#
# LIST THE COLUMN HEADERS FOR THE OUTPUT CSV FILE
# ------------------------------------------------#
def output_csv(posts, user, coms, commu):
    """
    Using the command line arguments, customise the column headers in
    the output CSV file according to what the user wants to research.

    Args:
        posts (str) : posts to scrape
        user (str) : user page to scrape
        coms (str) : comments to scrape
        commu (str) : communities to scrape
    
    Return:
        output_CSV_header (list) : list of column headers
    """

    # Bug : If the user did not put a value for posts, user, coms, or commu,
    # the variable 'output_spe[]' will have not been created. Consequently, at 
    # line 165, the concatenation will raise an error because the variable 
    # 'output_spe[]' doesn't exist.
    ## I : the user have to choose one, the script does not work if none 
    ## of the above is selected

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
    return output_base + output_spe


# ------------------------------------------------#
# CONCATENATE THE NAME OF THE OUTPUT CSV FILE
# ------------------------------------------------#
def name_csv(name, community, user, posts, coms, search, commu):
    """
    Using the command line arguments, customise the name of the CSV file
    that this program outputs.

    Args:
        name (str) : name of a community OR name of a user OR a keyword for a query 
        community (str) : community page to scrape
        user (str) : user page to scrape
        posts (str) : posts to scrape
        coms (str) : comments to scrape
        search (str) : search function to scrape
        commu (str) : communities to scrape
    
    Return:
        file_name_CSV (str) : name of the CSV file
    """
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


# ------------------------------------------------#
# SCRAPE A PAGE FROM REDDIT
# ------------------------------------------------#
def scrape_page(url): 
    """
    Using the URL, colect the data from the page(s)
    the user wants to scrape in json format.

    Args:
        url (str) :  URL to be requested and scraped 
        ## or url_first 
    
    Return:
        data (str) : data from the URL in json format
        after (str) : id of the next json page 
    """
    headers = {'user-agent': 'r2d2'}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    after = data['data']['after']
    return data, after ## getting the value for after here


# ------------------------------------------------#
# CLEAN DATA
# ------------------------------------------------#
def clean_data(data, user, posts, coms, commu):
    """
    Using the command line arguments and data, divise the data into 
    categories the user wants to scrape and select only the meaningfull 
    metadata associated in json format.

    Args:
        data (str) : data from the URL in json format
        name (str) :  name of a community OR name of a user OR a keyword for a query 
        community (str) : community page to scrape
        user (str) : user page to scrape
        posts (str) : posts to scrape
        coms (str) : comments to scrape
        search (str) : search function to scrape
        commu (str) : communities to scrape
    
    Return:
        result (list) : 
    """
    children = data['data']['children']
    results = [] ## creating a list to not write each row one by one
    for child in children:
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
        results.append(result)
    return results


# ------------------------------------------------#
# MAIN FUNCTION
# ------------------------------------------------#
def main():
    # ------------------------------------------------#
    # -- STEP 1 -- 
    # Parse the arguments passed to the command line

    community, user, search, posts, coms, commu, name = get_args()
    # Save their values as meaningful variables

    # ------------------------------------------------#
    # -- STEP 2 -- 
    # Open the CSV file and create a CSV writer object
    
    csv_file_name = name_csv(name, community, user, posts, coms, search, commu)
    # Give a name to the CSV file
    
    with open(csv_file_name, "w") as f: # Open the CSV file
        
        fieldnames = output_csv(posts, user, coms, commu) # Name the columns in the CSV file
        
        writer = csv.DictWriter(f, fieldnames=fieldnames) # Create the writer object
        
        writer.writeheader()
        # Write to the CSV the header row given by the writer parameter's 'fieldnames'

        # ------------------------------------------------#
        # -- STEP 3 -- 
        # Scrape page(s) and write the result to the CSV file

        # -- STEP 3.1 -- 
        # Scrape the landing page (first page)

        url = build_url(name, community, user, posts, coms, search, commu)
        # Customise the URL to be scraped according to the command line arguments
        
        data, after = scrape_page(url)
        # Scrape all the HTML from the URL given

        results = clean_data(data, user, posts, coms, commu)
        # Parse raw HTML data and return 1. cleaned data ('result') in a dictionary and
        # 2. the value of data['data']['after'] ('after')

        writer.writerows(results) # Write the cleaned result to the open CSV file

        # -- STEP 3.2 -- 
        # Scrape any pages following the landing page (first page)

        while after != None: 
            # If the last time 'clean_data()' was called and the function found 
            # that there was another page after the current one (aka 'after' does 
            # not equal an empty string), loop through this process one more time.
            ## changed after != '' to after != None 
            ## because the value of after when it has to stop is None and not ''

            after = f"&after={data['data']['after']}"

            url = build_url(name, community, user, posts, coms, search, commu, after)

            data, after = scrape_page(url)

            results = clean_data(data, user, posts, coms, commu)

            writer.writerows(results)




# This "boilerplate" tells python what to execute when this module
# (scrape_def_getagrs_reddig.py) is called from the command line.
# In this case, the boileplate will execute the function main(),
# which we have loaded up with all the secondary functions written
# to support the program's desired action. The goal is that these 
# secondary functions can be repurposed/recycled for other programs 
# because they have, ideally, been written with an attention to
# adaptability.
if __name__ == "__main__":
    main()

 