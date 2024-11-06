import json
import os 
import requests
import logging
from dotenv import load_dotenv  

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
BING_SEARCH_V7_SUBSCRIPTION_KEY = os.environ.get('BING_SEARCH_V7_SUBSCRIPTION_KEY')
assert BING_SEARCH_V7_SUBSCRIPTION_KEY

def bing_web_search(query: str) -> tuple[str, str]:
    load_dotenv()  # Add this line

    """
    Perform a Bing web search and return the headers and JSON response as formatted text.
    
    Args:
        query: Search query string
        
    Returns:
        Tuple of (headers_text, json_text)
    """
    logger.debug(f"Starting Bing web search for query: {query}")
    
    # Bing Search API endpoint
    endpoint = "https://api.bing.microsoft.com/v7.0/search"

    # Construct request
    mkt = 'en-US'
    params = { 'q': query, 'mkt': mkt }
    headers = { 'Ocp-Apim-Subscription-Key': BING_SEARCH_V7_SUBSCRIPTION_KEY }
    logger.debug(f"Constructed request with params: {params}")

    try:
        logger.debug(f"Sending GET request to {endpoint}")
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        
        headers_text = str(response.headers)
        json_text = json.dumps(response.json(), indent=2)
        logger.debug("JSON response: {}".format(json_text))
        
        logger.debug("Successfully retrieved and formatted response")
        return headers_text, json_text

    except Exception as ex:
        logger.error(f"Error in Bing web search: {ex}")
        print(f"Error details: {ex}")
        raise ex
    
def extract_urls_from_bing_results(json_response: str) -> list[str]:
    """
    Extract all URLs from the webPages section of Bing search results.
    
    Args:
        json_response: JSON string containing Bing search results
        
    Returns:
        List of URLs found in the webPages section
        
    Raises:
        json.JSONDecodeError: If the input is not valid JSON
        KeyError: If the expected JSON structure is not found
    """
    logger.debug("Starting URL extraction from Bing results")
    
    # Parse JSON string to dict
    try:
        data = json.loads(json_response)
        logger.debug("Successfully parsed JSON response")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        raise
    
    # Check if webPages section exists
    if 'webPages' not in data or 'value' not in data['webPages']:
        logger.warning("No webPages section found in response")
        return []
    
    # Extract URLs from each result in webPages
    urls = []
    for result in data['webPages']['value']:
        if 'url' in result:
            urls.append(result['url'])
    
    logger.debug(f"Extracted {len(urls)} URLs from response")        
    return urls