"""
News Library for Viola
Integrates with NewsAPI to fetch top headlines from India
"""

import requests

# NewsAPI endpoint and configuration
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# NewsAPI endpoint and configuration
# Get API key from environment variable or use placeholder
NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'YOUR_NEWSAPI_KEY')
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def get_india_news(language="en", country="in", category="general"):
    """
    Fetch top 5 news headlines from India using NewsAPI.
    
    Args:
        language (str): Language code (default: "en" for English)
        country (str): Country code (default: "in" for India)
        category (str): News category (general, business, entertainment, health, science, sports, technology)
    
    Returns:
        list: List of top 5 headlines as strings, or empty list if API call fails
    """
    
    # Check if API key is configured
    if NEWS_API_KEY == "YOUR_NEWSAPI_KEY":
        return ["Please configure your NewsAPI key in newsLibrary.py to use this feature."]
    
    try:
        # Prepare API request parameters
        params = {
            "country": country,
            "apiKey": NEWS_API_KEY,
            "pageSize": 5,  # Get top 5 headlines
            "sortBy": "publishedAt"
        }
        
        # Make API request
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse JSON response
        data = response.json()
        
        # Check if request was successful
        if data.get("status") != "ok":
            error_message = data.get("message", "Unknown error occurred")
            return [f"Error fetching news: {error_message}"]
        
        # Extract headlines from articles
        articles = data.get("articles", [])
        
        if not articles:
            return ["No news articles found."]
        
        # Format headlines
        headlines = []
        for i, article in enumerate(articles[:5], 1):
            title = article.get("title", "No title available")
            source = article.get("source", {}).get("name", "Unknown source")
            headline = f"Headline {i}: {title} from {source}"
            headlines.append(headline)
        
        return headlines
    
    except requests.exceptions.Timeout:
        return ["News API request timed out. Please try again later."]
    except requests.exceptions.ConnectionError:
        return ["Unable to connect to News API. Please check your internet connection."]
    except requests.exceptions.HTTPError as e:
        return [f"HTTP Error: {e.response.status_code}. Please check your API key."]
    except Exception as e:
        return [f"Error fetching news: {str(e)}"]

def setup_api_key(api_key):
    """
    Configure the NewsAPI key.
    Get your free API key at: https://newsapi.org/
    
    Args:
        api_key (str): Valid NewsAPI API key
    
    Returns:
        bool: True if key is set, False otherwise
    """
    global NEWS_API_KEY
    if api_key and len(api_key) > 10:
        NEWS_API_KEY = api_key
        return True
    return False
