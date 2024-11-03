import requests
from typing import Optional, List, Dict, Any, Tuple
from pydantic import ValidationError

from .schemas import CustomSearchResponse

class CustomSearchEngine:
    def __init__(self, api_key: str, engine_id: str, base_url: str = "https://customsearch.googleapis.com/customsearch/v1"):
        """
        Initialize the CustomSearchEngine with API key, engine ID, and optional base URL.
        
        :param api_key: Google API key for authentication.
        :param engine_id: ID of the custom search engine.
        :param base_url: Base URL for the Custom Search API.
        """
        self.api_key = api_key
        self.engine_id = engine_id
        self.base_url = base_url
        self.last_response = None  # Stores the last CustomSearchResponse object

    def search(self, query: str, **kwargs) -> Optional[CustomSearchResponse]:
        """
        Performs a search using the Google Custom Search API.
        
        :param query: The search term or phrase.
        :param kwargs: Additional search parameters (e.g., num, start, language, etc.).
        :return: An instance of CustomSearchResponse or None if an error occurs.
        """
        params = {
            "key": self.api_key,
            "cx": self.engine_id,
            "q": query,
            **kwargs
        }
        
        response = requests.get(self.base_url, params=params)
        
        if response.status_code == 200:
            try:
                self.last_response = CustomSearchResponse(**response.json())
                return self.last_response
            except ValidationError as e:
                print(f"Error parsing response: {e}")
        else:
            print(f"Request failed with status {response.status_code}: {response.text}")
        
        return None

    def get_total_results(self) -> int:
        """
        Returns the total number of results found in the last search response.
        
        :return: Total number of search results, or 0 if unavailable.
        """
        if self.last_response and self.last_response.searchInformation:
            return int(self.last_response.searchInformation.totalResults)
        return 0

    def get_search_time(self) -> float:
        """
        Returns the search time for the last query.
        
        :return: Time taken for the search in seconds, or 0 if unavailable.
        """
        if self.last_response and self.last_response.searchInformation:
            return self.last_response.searchInformation.searchTime
        return 0.0

    def get_items(self) -> List[Dict[str, Any]]:
        """
        Retrieves a simplified list of items (search results) from the last response.
        
        :return: A list of dictionaries with title, link, snippet, and displayLink of each result.
        """
        if self.last_response and self.last_response.items:
            return [{
                "title": item.title,
                "link": item.link,
                "snippet": item.snippet,
                "displayLink": item.displayLink
            } for item in self.last_response.items]
        return []

    def get_promotions(self) -> List[Dict[str, Any]]:
        """
        Retrieves promotions from the last response if any.
        
        :return: A list of dictionaries with details on promotions.
        """
        if self.last_response and self.last_response.promotions:
            return [{
                "title": promo.title,
                "link": promo.link,
                "displayLink": promo.displayLink,
                "bodyLines": promo.bodyLines
            } for promo in self.last_response.promotions]
        return []

    def get_corrected_query(self) -> Optional[str]:
        """
        Returns a spelling-corrected query if the API provided a suggestion.
        
        :return: Corrected query or None if unavailable.
        """
        if self.last_response and self.last_response.spelling:
            return self.last_response.spelling.correctedQuery
        return None

    def get_next_page_query(self) -> Optional[str]:
        """
        Retrieves the query terms for the next page if available.
        
        :return: Search terms for the next page or None if unavailable.
        """
        if self.last_response and self.last_response.queries.nextPage:
            return self.last_response.queries.nextPage[0].searchTerms
        return None

    def get_metadata(self) -> Dict[str, Any]:
        """
        Returns metadata from the last search context.
        
        :return: Dictionary of metadata information if available.
        """
        if self.last_response and self.last_response.context:
            return {
                "title": self.last_response.context.title,
                "facets": self.last_response.context.facets
            }
        return {}

    def get_pagemap_data(self) -> List[Dict[str, Any]]:
        """
        Retrieves page map data (metadata, images, etc.) from search results.
        
        :return: List of pagemap data dictionaries.
        """
        if self.last_response and self.last_response.items:
            return [item.pagemap for item in self.last_response.items if item.pagemap]
        return []

    def fetch_page(self, page_number: int) -> Optional[CustomSearchResponse]:
        """
        Fetches a specific page of results based on the page number.
        
        :param page_number: Page number to fetch.
        :return: CustomSearchResponse for the specified page or None if an error occurs.
        """
        if page_number < 1:
            print("Invalid page number. Page numbers start from 1.")
            return None

        start_index = (page_number - 1) * 10 + 1
        return self.search(query=self.last_response.queries.request[0].searchTerms, start=start_index)

    def display_results(self):
        """
        Prints a formatted display of the search results.
        """
        if not self.last_response or not self.last_response.items:
            print("No search results available.")
            return

        for index, item in enumerate(self.last_response.items, start=1):
            print(f"{index}. {item.title}")
            print(f"   URL: {item.link}")
            print(f"   Snippet: {item.snippet}\n")

    def __repr__(self):
        """
        Representation of the CustomSearchEngine instance.
        """
        return f"<CustomSearchEngine(engine_id={self.engine_id})>"

    @property
    def last_search_info(self) -> Optional[Dict[str, Any]]:
        """
        Returns summary of last search results, including total results, search time, etc.
        
        :return: Dictionary with search info or None if unavailable.
        """
        if self.last_response and self.last_response.searchInformation:
            return {
                "totalResults": self.last_response.searchInformation.totalResults,
                "searchTime": self.last_response.searchInformation.searchTime,
                "formattedTotalResults": self.last_response.searchInformation.formattedTotalResults,
                "formattedSearchTime": self.last_response.searchInformation.formattedSearchTime
            }
        return None
    
    def get_snippets(self) -> List[Tuple[str, str]]:
        """
        Returns a list of tuples containing plain and HTML snippets of each result.
        
        :return: List of (snippet, htmlSnippet) tuples.
        """
        if self.last_response and self.last_response.items:
            return [(item.snippet, item.htmlSnippet) for item in self.last_response.items]
        return []    