"""
DuckDuckGo search helper - no API key required.

Provides `web_search_summary(query)` which returns the instant answer or top result snippet.
"""
import requests


def web_search_summary(query: str) -> str:
    """Return a web search result for `query` using DuckDuckGo's instant answer API.
    
    Returns the instant answer if available, otherwise returns top result info.
    """
    if not query:
        return "No query provided."

    # DuckDuckGo Instant Answer API (no authentication needed)
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
    }

    try:
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()

        # Try to get instant answer first
        instant_answer = data.get("Answer")
        if instant_answer:
            return instant_answer

        # Try abstract (summary)
        abstract = data.get("AbstractText")
        if abstract:
            return abstract

        # Try to get first related topic
        related = data.get("RelatedTopics")
        if related and isinstance(related, list) and len(related) > 0:
            first = related[0]
            if isinstance(first, dict):
                text = first.get("Text")
                if text:
                    return text

        return "No results found for that query."
    except requests.exceptions.RequestException as e:
        return f"Error contacting DuckDuckGo: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
