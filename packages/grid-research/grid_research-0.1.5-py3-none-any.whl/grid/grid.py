from .bing_web_search import bing_web_search, extract_urls_from_bing_results
from .webpage_clean import webpage_to_text
from openai import OpenAI
from pydantic import BaseModel
from typing import List
import pandas as pd

class ColumnHeaders(BaseModel):
    headers: List[str]
    descriptions: List[str]

class ResearchData(BaseModel):
    data: List[List[str]]

class Grid:
    def __init__(self, client: OpenAI, num_rows: int, research_topic: str, headers: list = [], query: str = "", model: str = "gpt-4o"):
        self.headers = headers
        self.client = client
        self.research_topic = research_topic
        self.num_rows = num_rows
        self.query = query
        self.model = model

    def generate_headers(self) -> List[str]:
        if self.research_topic == "":
            raise ValueError("Research topic cannot be empty.")

        """Get column header suggestions from the LLM"""
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": "Generate up to 10 relevant column headers and their descriptions for organizing research data about the given topic."},
                {"role": "user", "content": f"Generate column headers for research about: {self.research_topic}"},
            ],
            response_format=ColumnHeaders,
        )
        return completion.choices[0].message.parsed.headers

    def generate_web_search_query(self) -> str:
        """
        Given user topic, headers generated and number of rows to generate, 
        Generate a web search query to help gather data
        Returns: A clean search query string without escape characters
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
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
                        "content": f"Generate a search query to find data about: {self.research_topic}\nRequired fields: {', '.join(self.headers)}\nNumber of rows needed: {self.num_rows}"
                    }
                ],
                temperature=0.7,
                max_tokens=100
            )        
            # Get the raw query and clean it up
            query = completion.choices[0].message.content
            # Remove any quotes and extra whitespace
            query = query.strip().strip('"').strip("'")
            self.query = query
            return query
        except Exception as e:
            raise Exception(f"Error generating search query: {str(e)}")
        
    def generate_research_data(self, urls: list[str]) -> pd.DataFrame:
        """Generate research data by reading webpages"""
        print("Generating research data...")
        
        # Initialize empty DataFrame with headers
        df = pd.DataFrame(columns=self.headers)
        
        for url in urls:
            print("Reading url: {0}".format(url))

            # Check if we have enough rows
            if len(df) >= self.num_rows:
                print(f"Reached desired number of rows ({self.num_rows}). Breaking URL loop.")
                break

            webpage_text = webpage_to_text(url)
            if webpage_text:
                try:
                    result = self.client.beta.chat.completions.parse(
                        model=self.model,
                        messages=[
                            { "role": "system", "content": 
                                f"""You are researcher. Your job is to read the internet webpage text and generate relevant data given the user query: {self.research_topic}
                                    in a table format. 
                                    The text may sometimes be totally irrelevant to the topic or headers. If this is the case just skip and return nothing
                                    The headers are: {self.headers}
                                    Make sure to generate data in this headers format
                                    The number of rows the user wants to fill out is: {self.num_rows}. Please generate this number or less
                                    Here is the webpage text: {webpage_text[:100000]}
                            """}
                        ],
                        temperature=0.7,
                        response_format=ResearchData
                    )
                    if result:
                        print("result: ", result)
                        data = result.choices[0].message.parsed.data
                        if data:
                            # Convert the list data to DataFrame and append
                            new_rows = pd.DataFrame(data[:self.num_rows - len(df)], columns=self.headers)
                            df = pd.concat([df, new_rows], ignore_index=True)
                    else:
                        print("No result for URL: {}".format(url))
                except Exception as e:
                    print(f"Skipping URL: {url} because of error {str(e)}")
            else:   
                print("---No text, Skipping URL: %s" % url)
        
        return df

    def bing_web_search(self, query: str = "") -> tuple[str, str]:
        if query == "" and self.query == "":
            raise Exception("Query cannot be empty. Please provide a valid research topic.")
        
        if query:
            self.query = query

        headers, json = bing_web_search(self.query)
        return headers, json

    def extract_urls_from_bing_web_search(self, json_response) -> List[str]:
        urls = extract_urls_from_bing_results(json_response)

        if len(urls) == 0:
            raise Exception("No URLs found in search results. Please try a different query.")
        
        return urls
    
    def research(self) -> pd.DataFrame:
        if not self.headers:
            print("Auto generating headers")
            self.headers = self.generate_headers()
        if not self.query:
            self.query = self.generate_web_search_query()

        headers, json = self.bing_web_search(self.query)
        urls = extract_urls_from_bing_results(json)
        data = self.generate_research_data(urls)
        return data

if __name__ == "__main__":
    import os
    c = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    grid = Grid(c, 100, "promising manufacturing startups", ["Name", "Funding", "Revenue", "Description"])
    data = grid.research()
    print(data)
    data.to_csv('manufacturing_startups.csv', index=False)
    

