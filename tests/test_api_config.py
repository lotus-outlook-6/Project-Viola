"""
Test script to verify API key is loaded from .env file
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import newsLibrary

print("API Key Configuration Test")
print("=" * 60)

if newsLibrary.NEWS_API_KEY == "YOUR_NEWSAPI_KEY":
    print("ERROR: API key not configured!")
    print("Please set up your .env file with your NewsAPI key.")
else:
    print(f"SUCCESS: API key loaded from .env file")
    print(f"Key length: {len(newsLibrary.NEWS_API_KEY)} characters")
    print(f"Key format valid: {newsLibrary.NEWS_API_KEY.isalnum()}")
    print("\nYour news feature is configured and ready to use!")

print("=" * 60)
