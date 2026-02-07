"""
Detailed news API test to verify API key works
"""
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import newsLibrary
import requests

print("Detailed NEWS API Test")
print("=" * 60)

print(f"API Key: {newsLibrary.NEWS_API_KEY[:10]}...{newsLibrary.NEWS_API_KEY[-4:]}")
print(f"API URL: {newsLibrary.NEWS_API_URL}")

print("\nMaking API request to NewsAPI...")
print("-" * 60)

params = {
    "country": "in",
    "apiKey": newsLibrary.NEWS_API_KEY,
    "pageSize": 5,
    "sortBy": "publishedAt"
}

try:
    response = requests.get(newsLibrary.NEWS_API_URL, params=params, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    print(f"API Status: {data.get('status')}")
    
    if data.get("status") == "ok":
        articles = data.get("articles", [])
        print(f"Articles Found: {len(articles)}")
        
        if articles:
            print("\nTop 5 Headlines:")
            for i, article in enumerate(articles[:5], 1):
                print(f"\n{i}. {article.get('title')}")
                print(f"   Source: {article.get('source', {}).get('name')}")
    else:
        print(f"Error: {data.get('message')}")
        print(f"Full Response: {json.dumps(data, indent=2)}")
        
except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")

print("\n" + "=" * 60)
