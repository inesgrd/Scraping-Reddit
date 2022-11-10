import json
import requests
import csv
from urllib.parse import quote_plus
from datetime import datetime
import argparse
import os

## Pb : duplicates when the number of comments or score changes during the scrapping
## need to clean the dataset after 
## find a way to say in the script ; a linkpost cannot appears twice (so do not take another the posts if already have this link?)

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
        type (str) : type of data to scrape, posts OR comments OR commu (indicates these are either posts or comments or communities to scrape)
        name (str) : name of a community OR a user OR a keyword for a query 
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-c", "--community", action="store_true", help="to scrape a community, only compatible with posts")
    group.add_argument("-u", "--user", action="store_true", help="to scrape a user, only compatible with posts OR comments")
    group.add_argument("-s", "--search", action="store_true", help="to scrape a search page, only compatible with posts OR commu")

    parser.add_argument("-t", "--type", default="posts", choices=["posts", "comments", "commu"], help="indicate what type of data you want to scrape, only choose one and be careful it is a working combination: -> posts and community OR user OR search, -> comments and user, -> commu and search")

    parser.add_argument("name", help="either the name of the community OR the name of an user OR the keyword searched in Reddit")

    args = parser.parse_args()

    community = args.community
    user = args.user
    search = args.search
    type = args.type
    name = args.name

    return community, user, search, type, name

community, user, search, type, name = get_args()

# ------------------------------------------------#
# VERIFY ARGUMENTS PASSED FROM THE COMMAND LINE
# ------------------------------------------------#
def test_error(community, user, search, type):
    """
    Using the command line arguments, verify their combinaison 
    is possible to scrape data from Reddit

    Reminder : 
    -> community and posts
    -> user and posts OR comments
    -> search and posts OR commu

    Args:
        community (str) : community page to scrape
        user (str) : user page to scrape
        search (str) : search function to scrape 
        type (str) : type of data to scrape, posts OR comments OR commu

    Return:
        error (str) : indicates there is an error and what is possible
    """
    if community:
        if type == 'posts':
            error = None
        if type == 'comments':
            error = 'Sorry this query is impossible ! See help for a working combination, community only posible with posts'
        if type == 'commu':
            error = 'Sorry this query is impossible ! See help for a working combination, community only posible with posts'
    elif user:
        if type == 'posts' or type == 'comments':
             error = None
        if type == 'commu':
            error = 'Sorry this query is impossible ! See help for a working combination, user only posible with posts OR comments'
    elif search:
        if type == 'posts' or type == 'commu':
             error = None
        if type == 'comments':
            error = 'Sorry this query is impossible ! See help for a working combination, search only posible with posts OR commu'
    return error

# ------------------------------------------------#
# CONCATENATE A URL TO SCRAPE
# ------------------------------------------------#
def build_url(community, user, search, type, name, after=""): 
    """
    Using the command line arguments, concatenate the URL needed to access
    the Reddit page(s) that the user wants to scrape.

    Args: 
        community (str) : community page to scrape
        user (str) : user page to scrape
        search (str) : search function to scrape 
        type (str) : type of data to scrape, posts OR comments OR commu
        name (str) : name of a community OR name of a user OR a keyword for a query
        after (str) : id of the next json page OR null/void here

    Return:
        url (str) : URL to be requested and scraped
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
        if type == 'posts':     
            page = 'submitted'
        elif type == 'comments':    
            page = 'comments'
        url = f'{reddit_url}/{path}/{name}/{page}{f_json}{after}{sort}'
    elif search:
        path = 'search'
        if type == 'posts':
            sort = '&sort=new'
            if '/' in name:
                name = f'url:{name}'
                url = f'{reddit_url}/{path}{f_json}{after}&q={quote_plus(name)}&type=link{sort}'
            elif '/' not in name:
                url = f'{reddit_url}/{path}{f_json}{after}&q={name}{sort}'
        elif type == 'commu':
            sort = '&type=sr'
            url = f'{reddit_url}/{path}{f_json}{after}&q={name}{sort}'
    return url


# ------------------------------------------------#
# LIST THE COLUMN HEADERS FOR THE OUTPUT CSV FILE
# ------------------------------------------------#
def output_csv(type, user):
    """
    Using the command line arguments, customise the column headers in
    the output CSV file according to what the user wants to research.

    Args:
        type (str) : type of data to scrape, posts OR comments OR commu
        user (str) : user page to scrape
    
    Return:
        output_CSV_header (list) : list of column headers
    """
    output_base = [
        "subreddit",
        "subreddit_id",
        "link_post",
        "date_utc",
    ]
    if type == 'posts':
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
    elif type == 'comments':
            output_spe = [
                "title_post",
                "author_post",
                "text_com",
                "link_joined",
                "score_com",
                "comments_post",
                "awards_com"
            ]
    elif type == 'commu':
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
def name_csv(community, user, search, type, name):
    """
    Using the command line arguments, customise the name of the CSV file
    that this program outputs.

    Args:
        community (str) : community page to scrape
        user (str) : user page to scrape
        search (str) : search function to scrape
        type (str) : type of data to scrape, posts OR comments OR commu
        name (str) : name of a community OR name of a user OR a keyword for a query 
    
    Return:
        csv_file_name (str) : name of the CSV file
    """
    if community:
        csv_file_name = f'community_posts_{name}_scraping_reddit.csv'
    elif user:
        if type == 'posts':
            csv_file_name = f'user_posts_{name}_scraping_reddit.csv'
        elif type == 'comments':
            csv_file_name = f'user_comments_{name}_scraping_reddit.csv'
    elif search:
        if type == 'posts':
            if '/' in name:
                csv_file_name = f'search_posts_url_scraping_reddit.csv'
            if '/' not in name:
                csv_file_name = f'search_posts_{name}_scraping_reddit.csv'
        elif type == 'commu':
            csv_file_name = f'search_commu_{name}_scraping_reddit.csv'
    return csv_file_name


# ------------------------------------------------#
# SCRAPE A PAGE FROM REDDIT
# ------------------------------------------------#
def scrape_page(url): 
    """
    Using the URL, colect the data from the page(s)
    the user wants to scrape in json format.

    Args:
        url (str) :  URL to be requested and scraped
    
    Return:
        data (str) : data from the URL in json format
        after (str) : id of the next json page 
    """
    headers = {'user-agent': 'r2d2'}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    after = data['data']['after']
    return data, after


# ------------------------------------------------#
# CLEAN DATA
# ------------------------------------------------#
def clean_data(data, type, user):
    """
    Using the command line arguments and data, divise the data into 
    categories the user wants to scrape and select only the meaningfull 
    metadata associated in json format.

    Args:
        data (str) : data from the URL in json format
        type (str) : type of data to scrape, posts OR comments OR commu
        user (str) : user page to scrape
    
    Return:
        result (list) : results in json format
    """
    children = data['data']['children']
    results = []
    for child in children:
        child = child['data']
        result = {
            "date_utc": datetime.utcfromtimestamp(int(child['created_utc'])).isoformat()
        }
        if type == 'posts':
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
        elif type == 'comments':
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
        elif type == 'commu':
            result["subreddit"] = child["display_name"]
            result["subreddit_name"] = child["title"]
            result["subreddit_id"] = child["name"]
            result["subreddit_subscribers"] = child["subscribers"]
            result["link_post"] = 'https://www.reddit.com{permalink}'.format(permalink = child["url"])
            result["description_subreddit"] = child["public_description"]
            result["rules_of_publication_subreddit"] = child["submit_text"]
        results.append(result)
    if len(results) > 0:
        return results


# ------------------------------------------------#
# MAIN FUNCTION
# ------------------------------------------------#
def main():
    # ------------------------------------------------#
    # -- STEP 1 -- 
    # Parse the arguments passed to the command line

    community, user, search, type, name = get_args()
    # Save their values as meaningful variables

    # -- STEP 1.1 --
    # Verify is the combination of the arguments passed to the command line is possible

    error = test_error(community, user, search, type)
    # Return error if there is any ortherwise error is None

    if error is not None:
        print(error)
        exit()
        # Stop the script if there is any
    else : 

    # ------------------------------------------------#
    # -- STEP 2 -- x
    # Open the CSV file and create a CSV writer object
    
        csv_file_name = name_csv(community, user, search, type, name)
        # Give a name to the CSV file
        
        file_exist = os.path.isfile(csv_file_name)

        with open(csv_file_name, "w") as f: # Open the CSV file
            
            fieldnames = output_csv(type, user) # Name the columns in the CSV file
            
            writer = csv.DictWriter(f, fieldnames=fieldnames) # Create the writer object
            
            if not file_exist: 
                writer.writeheader()
            # Write to the CSV the header row given by the writer parameter's 'fieldnames'

            # ------------------------------------------------#
            # -- STEP 3 -- 
            # Scrape page(s) and write the result to the CSV file

            # -- STEP 3.1 -- 
            # Scrape the landing page (first page)

            url = build_url(community, user, search, type, name)
            # Customise the URL to be scraped according to the command line arguments
            
            data, after = scrape_page(url)
            # Scrape all the HTML from the URL given

            results = clean_data(data, type, user)

            # Parse raw HTML data and return 1. cleaned data ('result') in a dictionary and
            # 2. the value of data['data']['after'] ('after')
            if results:
                writer.writerows(results) # Write the cleaned result to the open CSV file

            # -- STEP 3.2 -- 
            # Scrape any pages following the landing page (first page)

            while after != None: 
                # If the last time 'clean_data()' was called and the function found 
                # that there was another page after the current one (aka 'after' does 
                # not equal an empty string), loop through this process one more time.

                after = f"&after={data['data']['after']}"

                url = build_url(community, user, search, type, name, after)

                data, after = scrape_page(url)

                results = clean_data(data, type, user)

                if results:
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