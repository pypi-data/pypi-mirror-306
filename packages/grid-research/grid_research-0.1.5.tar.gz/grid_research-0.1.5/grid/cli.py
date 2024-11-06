import openai
from colorama import init, Fore, Back, Style
from pydantic import BaseModel
from typing import List, Dict
from openai import OpenAI
from .utils.bing_web_search import bing_web_search, extract_urls_from_bing_results
from .utils.webpage_clean import webpage_to_text
import os
import logging
import csv
from dotenv import load_dotenv  
load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
assert OPENAI_API_KEY

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ColumnHeaders(BaseModel):
    headers: List[str]
    descriptions: List[str]

class ResearchData(BaseModel):
    data: List[List[str]]

def display_welcome_banner():
    """Display a styled welcome banner with tagline and description"""
    logger.debug("Displaying welcome banner")
    print("\n" + "="* 50)
    print(Fore.CYAN + Style.BRIGHT + """                      

      ___           ___                       ___     
     /\  \         /\  \          ___        /\  \    
    /::\  \       /::\  \        /\  \      /::\  \   
   /:/\:\  \     /:/\:\  \       \:\  \    /:/\:\  \  
  /:/  \:\  \   /::\~\:\  \      /::\__\  /:/  \:\__\ 
 /:/__/_\:\__\ /:/\:\ \:\__\  __/:/\/__/ /:/__/ \:|__|
 \:\  /\ \/__/ \/_|::\/:/  / /\/:/  /    \:\  \ /:/  /
  \:\ \:\__\      |:|::/  /  \::/__/      \:\  /:/  / 
   \:\/:/  /      |:|\/__/    \:\__\       \:\/:/  /  
    \::/  /       |:|  |       \/__/        \::/__/   
     \/__/         \|__|                     ~~       

    """ + Style.RESET_ALL)
    print(Fore.YELLOW + Style.BRIGHT + "〔 Grid 〕" + Style.RESET_ALL)
    print(Fore.MAGENTA + "An AI powered CLI to make you a freak in the (spread)sheets" + Style.RESET_ALL)
    print("="* 50)
    
    # Description section
    print(Fore.WHITE + Style.BRIGHT + "\n🔍 What is Grid?" + Style.RESET_ALL)
    print(Fore.CYAN + """Grid is your AI-powered research companion that transforms
raw topics into structured, spreadsheet-ready data.

Features:""" + Style.RESET_ALL)
    
    features = [
        "🤖 AI-suggested column headers with descriptions",
        "✏️  Custom header editing and creation",
        "📊 Generates 1-100 rows of research data",
        "🎨 Beautiful terminal interface",
        "📋 Export-ready structured data"
    ]
    
    for feature in features:
        print(Fore.GREEN + f"  • {feature}" + Style.RESET_ALL)
        
    print("\n" + "="* 50 + "\n")

def get_ai_suggested_headers(client, research_topic):
    """Get column header suggestions from OpenAI"""
    logger.debug(f"Getting AI suggested headers for topic: {research_topic}")
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "Generate up to 10 relevant column headers and their descriptions for organizing research data about the given topic."},
                {"role": "user", "content": f"Generate column headers for research about: {research_topic}"},
            ],
            response_format=ColumnHeaders,
        )
        logger.debug(f"Successfully got AI header suggestions: {completion.choices[0].message.parsed}")
        return completion.choices[0].message.parsed
    except Exception as e:
        logger.error(f"Error getting AI suggestions: {str(e)}")
        print(Fore.RED + f"Error getting AI suggestions: {str(e)}" + Style.RESET_ALL)
        return None
    
def generate_web_search_query(client: OpenAI, topic: str, headers: list[str], num_rows: int) -> str:
    """
    Given user topic, headers generated and number of rows to generate, 
    Generate a web search query to help gather data
    Returns: A clean search query string without escape characters
    """
    logger.debug(f"Generating web search query for topic: {topic}, headers: {headers}, num_rows: {num_rows}")
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are an AI web research assistant specialized in crafting precise search queries. Your goal is to generate search queries that will help find structured data matching the user's requirements.
                    Follow these guidelines when generating queries:
                    2. Include relevant technical or industry-specific terms
                    5. Target authoritative sources (e.g., government databases, research institutions)

                    For each query request, you will receive:
                        - A topic describing the data needed
                        - Headers indicating required data fields
                        - Number of rows of data desired

                        Respond with ONLY the search query text, without any quotes or formatting.
                        
                        Example input:
                        Topic: "US population by state"
                        Headers: ["State", "Population", "Year"]
                        Rows: 50

                        Example output:
                        US population by state data table census

                        Keep queries concise but comprehensive enough to find relevant structured data."""
                },
                {
                    "role": "user",
                    "content": f"Generate a search query to find data about: {topic}\nRequired fields: {', '.join(headers)}\nNumber of rows needed: {num_rows}"
                }
            ],
            temperature=0.7,
            max_tokens=100
        )        
        # Get the raw query and clean it up
        query = completion.choices[0].message.content
        
        # Remove any quotes and extra whitespace
        query = query.strip().strip('"').strip("'")
        
        logger.debug(f"Generated search query: {query}")
        return query
    except Exception as e:
        logger.error(f"Error generating search query: {str(e)}")
        raise Exception(f"Error generating search query: {str(e)}")

def generate_research_data(client: OpenAI, urls: list[str], num_rows: int, topic: str, headers: list[str]) -> list[list]:
    """Generate research data by reading webpages"""
    logger.debug(f"Generating research data for topic: {topic}, num_rows: {num_rows}")
    print("Generating research data...")
    
    # Create CSV file with headers
    with open('research_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
    
    data: ResearchData = []
    for url in urls:
        logger.debug(f"Processing URL: {url}")
        webpage_text = webpage_to_text(url)
        if webpage_text:
            try:
                result = client.beta.chat.completions.parse(
                    model="gpt-4o-2024-08-06",
                    messages=[
                        { "role": "system", "content": 
                            f"""You are researcher. Your job is to read the internet webpage text and generate relevant data given the user query: {topic}
                                in a table format. 
                                The text may sometimes be totally irrelevant to the topic or headers. If this is the case just skip and return nothing
                                The headers are: {headers}
                                Make sure to generate data in this headers format
                                The number of rows the user wants to fill out is: {num_rows}. Please generate this number or less
                                Here is the webpage text: {webpage_text[:250000]}
                        """}
                    ],
                    temperature=0.7,
                    response_format=ResearchData
                )
                if result:
                    print("result: ", result)
                    print(result.choices[0].message.parsed.data)
                    logger.debug(f"Generated {len(result.choices[0].message.parsed.data)} rows of data from URL: {url}")
                    new_data = result.choices[0].message.parsed.data[:num_rows]
                    data.extend(new_data)
                    
                    # Append new data to CSV file
                    with open('research_data.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerows(new_data)

                    # Check if we have enough rows
                    if len(data) >= num_rows:
                        logger.debug(f"Reached desired number of rows ({num_rows}). Breaking URL loop.")
                        break
                else:
                    logger.debug("No result for URL: {}".format(url))
            except Exception as e:
                logger.error(f"Error generating research data for URL {url}: {str(e)}")
                raise Exception("Error generating research data for URL: %s" % url)
        else:   
            logger.warning(f"No text content found for URL: {url}")
            print("---No text, Skipping URL: %s" % url) 
    logger.debug(f"Total rows of research data generated: {len(data)}")
    return data

def display_headers(headers, descriptions):
    """Display headers with their descriptions"""
    logger.debug("Displaying headers and descriptions")
    print("\n" + Fore.CYAN + "Suggested Column Headers:" + Style.RESET_ALL)
    for idx, (header, desc) in enumerate(zip(headers, descriptions), 1):
        print(f"{idx}. {Fore.GREEN}{header}{Style.RESET_ALL}")
        print(f"   {Fore.YELLOW}Description: {desc}{Style.RESET_ALL}")

def edit_headers(headers):
    """Allow user to edit headers"""
    logger.debug("Starting header editing")
    print(Fore.CYAN + "\nCurrent headers:" + Style.RESET_ALL)
    for idx, header in enumerate(headers, 1):
        print(f"{idx}. {header}")
    
    while True:
        print(Fore.YELLOW + "\nEdit options:" + Style.RESET_ALL)
        print("1. Remove header")
        print("2. Add header")
        print("3. Modify header")
        print("4. Done editing")
        
        choice = input(Fore.GREEN + "Choose an option (1-4): " + Style.RESET_ALL)
        logger.debug(f"User selected edit option: {choice}")
        
        if choice == '1':
            idx = int(input("Enter header number to remove: ")) - 1
            if 0 <= idx < len(headers):
                removed_header = headers.pop(idx)
                logger.debug(f"Removed header: {removed_header}")
        elif choice == '2':
            if len(headers) < 10:
                new_header = input("Enter new header: ")
                headers.append(new_header)
                logger.debug(f"Added new header: {new_header}")
            else:
                logger.warning("Attempted to add header when maximum reached")
                print(Fore.RED + "Maximum 10 headers allowed!" + Style.RESET_ALL)
        elif choice == '3':
            idx = int(input("Enter header number to modify: ")) - 1
            if 0 <= idx < len(headers):
                old_header = headers[idx]
                new_header = input("Enter new header name: ")
                headers[idx] = new_header
                logger.debug(f"Modified header from '{old_header}' to '{new_header}'")
        elif choice == '4':
            break
    
    logger.debug(f"Final headers after editing: {headers}")
    return headers

def get_row_count():
    """Get the number of rows to generate from user"""
    logger.debug("Getting row count from user")
    while True:
        try:
            print(Fore.YELLOW + "\nHow many rows of research data would you like to generate? (1-100)" + Style.RESET_ALL)
            rows = int(input(Fore.GREEN + "Enter number of rows: " + Style.RESET_ALL))
            if 1 <= rows <= 100:
                logger.debug(f"User selected {rows} rows")
                return rows
            logger.warning(f"Invalid row count entered: {rows}")
            print(Fore.RED + "Please enter a number between 1 and 100." + Style.RESET_ALL)
        except ValueError:
            logger.warning("Invalid input for row count")
            print(Fore.RED + "Please enter a valid number." + Style.RESET_ALL)

def main():
    logger.info("Starting Grid application")
    init()  # Initialize colorama
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    display_welcome_banner()
    # Get research topic
    print(Fore.GREEN + "What would you like to research?" + Style.RESET_ALL)
    research_topic = input(Fore.WHITE + "→ " + Style.RESET_ALL)
    logger.debug(f"User entered research topic: {research_topic}")
    
    # Ask user preference for headers
    print(Fore.YELLOW + "\nHow would you like to create your column headers?" + Style.RESET_ALL)
    print("1. Get AI suggestions")
    print("2. Create manually")
    choice = input(Fore.GREEN + "Choose an option (1 or 2): " + Style.RESET_ALL)
    logger.debug(f"User selected header creation method: {choice}")
    
    headers = []
    
    if choice == '1':
        # Get AI suggestions
        result = get_ai_suggested_headers(client, research_topic)
        if result:
            display_headers(result.headers, result.descriptions)
            headers = result.headers.copy()
            
            # Ask if user wants to edit suggestions
            edit_choice = input(Fore.YELLOW + "\nWould you like to edit these headers? (y/n): " + Style.RESET_ALL)
            logger.debug(f"User chose to edit headers: {edit_choice.lower() == 'y'}")
            if edit_choice.lower() == 'y':
                headers = edit_headers(headers)
    else:
        # Manual creation
        logger.debug("User creating headers manually")
        print(Fore.CYAN + "\nEnter your headers (maximum 10, press Enter with empty input to finish):" + Style.RESET_ALL)
        while len(headers) < 10:
            header = input(f"Header {len(headers) + 1}: ")
            if not header:
                break
            headers.append(header)
            logger.debug(f"Added manual header: {header}")
    
    # Get number of rows to generate
    num_rows = get_row_count()
    
    # Generate research data
    print(Fore.YELLOW + f"\nGenerating {num_rows} rows of research data..." + Style.RESET_ALL)
    query = generate_web_search_query(client, research_topic, headers, num_rows)
    logger.debug(f"Performing web search with query: {query}")
    headers_response, json_response = bing_web_search(query)
    urls = extract_urls_from_bing_results(json_response)

    if len(urls) == 0:
        raise Exception("No URLs found in search results. Please try a different query.")
    
    logger.debug(f"Extracted {len(urls)} URLs from search results")
    research_data = generate_research_data(client, urls, num_rows, research_topic, headers)
    logger.debug(f"Generated research data: {research_data}")
    print("research data: ", research_data)
    print(Fore.GREEN + "\nResearch data generation complete!" + Style.RESET_ALL)
    logger.info("Grid application completed successfully")

if __name__ == "__main__":
    main()