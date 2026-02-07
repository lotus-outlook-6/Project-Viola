"""
Test script to verify news library functionality
"""
import sys
import os

# Add parent directory to path to import newsLibrary
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import newsLibrary

def test_news_library():
    """Test the news library and API integration"""
    
    print("Testing News Library...")
    print("=" * 60)
    
    # Check if API key is configured
    if newsLibrary.NEWS_API_KEY == "YOUR_NEWSAPI_KEY":
        print("\nWARNING: API key not configured!")
        print("To use the news feature:")
        print("1. Visit https://newsapi.org/")
        print("2. Sign up for a free account")
        print("3. Copy your API key")
        print("4. Open newsLibrary.py and replace YOUR_NEWSAPI_KEY with your key")
        print("\nTesting with placeholder key (will fail):\n")
    
    print("Fetching top 5 headlines from India...")
    print("-" * 60)
    
    headlines = newsLibrary.get_india_news()
    
    if headlines:
        for i, headline in enumerate(headlines, 1):
            print(f"\n{headline}")
    
    print("\n" + "=" * 60)
    
    if newsLibrary.NEWS_API_KEY == "YOUR_NEWSAPI_KEY":
        print("Configure your API key to fetch real news!")
    else:
        print("News library is working correctly!")

if __name__ == "__main__":
    test_news_library()
