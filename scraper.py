import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
from csv import writer
import re
import json

# Global Variables
exclude_list = ['http://shakespeare.mit.edu/news.html','http://shakespeare.palomar.edu/', 'http://www.python.org/~jeremy/',
'http://tech.mit.edu/', 'http://shakespeare.mit.edu/Shakespeare', 'full.html']

root = 'http://shakespeare.mit.edu/'
amazon = 'amazon.com'

#=====================================================================================================
def fetchFromURL(url):

    """
    Attempt to fetch content from URL via HTTP GET request. If it's HTML/XML return otherwise
    don't do anything

    """

    try:

        with closing(get(url, stream=True)) as resp:

            if is_good_response(resp):

                return resp.content

            else:

                return None

 

    except RequestException as e:

        log_error('Error during request to {0}:{1}' . format(url, str(e)))

        return None

def is_good_response(resp):

    """
    Returns True if response looks like HTML
    """

    content_type = resp.headers['Content-Type'].lower()

    return (resp.status_code == 200

            and content_type is not None

            and content_type.find('html') > -1)

def log_error(e):

    """
    log those errors or you'll regret it later...
    """

    print(e)

def get_target_urls(target): # edited: returns a list of urls

    url_list = []
    
    """
    Example of isolating different parent elements to gather subsequent URLs
    """

    soup = BeautifulSoup(target, 'html.parser')

    for row in soup.find_all('td'):
        
        for link in row.find_all('a'):

            url = link.get('href')
            
            url_list.append(url)

   
    return url_list

def get_second_target(target): # Made this based off above
    
    url_list = []
    
    """
    Example of isolating different parent elements to gather subsequent URLs
    """

    soup = BeautifulSoup(target, 'html.parser')

    for row in soup.find_all('p'):
        
        for link in row.find_all('a'):

            url = link.get('href')
            
            url_list.append(url)
 
    return url_list

def pull_text(target): # Strips html from webpage and saves to .txt file

    path = os.getcwd() + '/docs'
    if '/docs' not in os.getcwd():
        os.chdir(path)

    # Pulls HTML from page
    url = target    
    r = requests.get(url)

    page_text = r.text

    # Formatting file name
    filename = target
    filename = filename.replace('http://shakespeare.mit.edu/', "")
    filename = filename.replace('.html', '')
    filename = filename.replace("/", "_")
    filename = filename.replace(".", "-")
    filename = filename + ".txt"

    # Create file with formatted name and text from page
    f = open(filename, 'w')

    soup = BeautifulSoup(page_text, 'html.parser')
    soup = soup.get_text()
    
    reg = re.compile('[^a-zA-Z]')
    soup = reg.sub(' ', soup)
    soup = soup.lower()

    f.write(soup)  

    f.close()

    return filename

# =====================================================================================================     

def main():
    
    print("Program Started...")

    print("Get comfortable, this takes a while...")

    # All Lists needed
    landing_url_list = []
    all_text_list_tokenized = []  # all words post tokenization
    second_url_list = []          # all urls in first page
    third_url_list = []           # all urls in second page
    
    # =================================
    # SCRAPING LANDING PAGE
    # =================================

    path = os.getcwd() + '/docs'
    
    # creates directory for all text files from webpages
    os.mkdir(path) 

    # raw html from landing page
    landing_html = fetchFromURL(root) 
    soup = BeautifulSoup(landing_html, 'html.parser')

    # Gets urls from landing page
    urls = get_target_urls(landing_html) 

    for link in urls:
        if link in exclude_list:
            # skip unwanted links
            continue
        else:
            landing_url_list.append(link)   
    
    # =================================
    # SCRAPING SECOND PAGE
    # =================================

    # iterates through links on landing page
    for link in landing_url_list:

        # Page after Landing page
        link = root + link 
        second_html = fetchFromURL(link)
        second_soup = BeautifulSoup(second_html, 'html.parser')

        # gets urls from page after landing page
        urls = get_second_target(second_html) 

        if len(urls) == 0: 
            filename = pull_text(link) 
                
        else: #only gets it if its one act. Not full.
            for url in urls:
                if amazon in url:
                    continue

                elif url in exclude_list:
                    continue
                
                else:
                    if url not in second_url_list:
                        second_url = link.replace("index.html", url)

                        # writes text of page to text file in /docs directory
                        filename = pull_text(second_url)     
main()