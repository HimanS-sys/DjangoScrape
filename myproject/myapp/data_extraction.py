from urllib.parse import urlparse
from bs4 import BeautifulSoup, NavigableString
import time
import random
import requests
import re


def normalize_url(url):
    parsed_url = urlparse(url)
    if not parsed_url.path.endswith('/'):
        url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}/"
    return url

def scrape_content_2(domain_url):
    try:
        response = requests.get(domain_url)
        soup = BeautifulSoup(response.text, "html.parser")
        scraped_content = []
        id_set = fetch_ids_from_href(domain_url)
        for section_id, section_name in id_set:
            time.sleep(random.randint(6, 10))
            section_soup = soup.find_all(id = section_id)[0]
            content = list(extract_text_from_parents_2(section_soup))
            scraped_content.append({section_name : content})

    except Exception as e:
        print(f"Error scraping content: {str(e)}")

    return scraped_content

def extract_text_from_parents_2(soup):
    # Fetch the webpage content
        # Find all leaf tags
    leaf_tags = soup.find_all(lambda tag: not tag.find(recursive = False))
    parent_texts = set()
    # Extract text content from parent tags of leaf tags
    for tag in leaf_tags:
        parent = tag.parent
        text = parent.get_text(separator = " ", strip = True)
        text = re.sub(r'\s+', ' ', text)
        if text:
            parent_texts.add(text)
    return parent_texts


def fetch_ids_from_href(url):
    '''
    use base url to create a list of ids all the section
    of the Single Page Application  
    '''

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    sections_from_href = set()

    for link in links:
        href = link["href"]
        if "#" in href:
            section_id = href.split("#")[-1]
            text_content = link.get_text(strip=True)
            sections_from_href.add((section_id, text_content))

    return sections_from_href