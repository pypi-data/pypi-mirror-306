from typing import List, Optional, Dict, Any
from pydantic import BaseModel

"""
This module defines the Pydantic models for parsing the response from the Custom Search API.
"""

class Url(BaseModel):
    """
    Represents the URL information in the response. 
    """
    type: str
    template: str


class Query(BaseModel):
    """
    Represents a query in the response. This can be used to represent previousPage, request, or nextPage queries.
    """
    title: str
    totalResults: str
    searchTerms: str
    count: int
    startIndex: int
    startPage: Optional[int] = None
    language: Optional[str] = None
    inputEncoding: Optional[str] = None
    outputEncoding: Optional[str] = None
    safe: Optional[str] = None
    cx: Optional[str] = None
    sort: Optional[str] = None
    filter: Optional[str] = None
    gl: Optional[str] = None
    cr: Optional[str] = None
    googleHost: Optional[str] = None
    disableCnTwTranslation: Optional[str] = None
    hq: Optional[str] = None
    hl: Optional[str] = None
    siteSearch: Optional[str] = None
    siteSearchFilter: Optional[str] = None
    exactTerms: Optional[str] = None
    excludeTerms: Optional[str] = None
    linkSite: Optional[str] = None
    orTerms: Optional[str] = None
    relatedSite: Optional[str] = None
    dateRestrict: Optional[str] = None
    lowRange: Optional[str] = None
    highRange: Optional[str] = None
    fileType: Optional[str] = None
    rights: Optional[str] = None
    searchType: Optional[str] = None
    imgSize: Optional[str] = None
    imgType: Optional[str] = None
    imgColorType: Optional[str] = None
    imgDominantColor: Optional[str] = None


class Queries(BaseModel):
    """
    Represents the queries in the response, including previousPage, request, and nextPage.
    """
    previousPage: Optional[List[Query]] = None
    request: List[Query]
    nextPage: Optional[List[Query]] = None


class Promotion(BaseModel):
    """
    Represents a promotion/advertisement in the search results.
    """
    title: str
    link: str
    displayLink: str
    bodyLines: Optional[List[Dict[str, str]]] = None  # Assuming a list of dictionaries, adjust as needed


class Context(BaseModel):
    """
    Represents the context information in the response. i.e., the context of the search.
    """
    title: Optional[str] = None
    facets: Optional[List[List[Dict[str, Any]]]] = None  # Assumes a nested structure, adjust as needed


class SearchInformation(BaseModel):
    """
    Represents the search information in the response. i.e., the search time, total results, etc.
    """
    searchTime: float
    formattedSearchTime: str
    totalResults: str
    formattedTotalResults: str


class Spelling(BaseModel):
    """
    Represents the spelling information in the response. i.e., the corrected query.
    """
    correctedQuery: Optional[str] = None
    htmlCorrectedQuery: Optional[str] = None


class Pagemap(BaseModel):
    """
    Represents the page map information in the response. i.e., metadata, thumbnails, etc.
    """
    metatags: Optional[List[Dict[str, Any]]] = None
    cse_thumbnail: Optional[List[Dict[str, Any]]] = None
    hcard: Optional[List[Dict[str, Any]]] = None
    imageobject: Optional[List[Dict[str, Any]]] = None
    person: Optional[List[Dict[str, Any]]] = None
    cse_image: Optional[List[Dict[str, Any]]] = None


class Result(BaseModel):
    """
    Represents an individual search result in the response.
    """
    kind: str
    title: str
    htmlTitle: str
    link: str
    displayLink: str
    snippet: str
    htmlSnippet: str
    formattedUrl: str
    htmlFormattedUrl: str
    pagemap: Optional[Pagemap] = None


class CustomSearchResponse(BaseModel):
    """
    Represents the response from a custom search API.
    """
    kind: str
    url: Url
    queries: Queries
    promotions: Optional[List[Promotion]] = None
    context: Optional[Context] = None
    searchInformation: SearchInformation
    spelling: Optional[Spelling] = None
    items: Optional[List[Result]] = None  # Could be empty if no results