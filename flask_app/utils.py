import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from ..logger_config import logger

def google_search(query, num_results=2):
    '''
    scrape top 2 ariticle from google search
    '''
    search_url = f"https://www.google.com/search?q={quote_plus(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = []
        
        for g in soup.find_all('div', class_='yuRUbf')[:num_results]:
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                search_results.append(link)
        
        logger.info(f"Found {len(search_results)} results for query: {query}")
        return search_results
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return []
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return []
    
if __name__ == "__main__":
    google_search()