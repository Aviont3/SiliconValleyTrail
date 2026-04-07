import os
import json

import urllib.request
import ssl
import certifi




url = "https://newsapi.org/v2/top-headlines/sources?category=technology&apiKey=4cd4684dc97d44e294b2241534dfa5f3" + os.getenv("News_Api_Key")

request = urllib.request.Request(url)
context = ssl.create_default_context(cafile=certifi.where())
with urllib.request.urlopen(request, context=context) as response:
    news_data = json.load(response) 
print("\n" + "="*120)
print("TOP TECHNOLOGY NEWS SOURCES".center(120))
print("="*120 + "\n")
for source in news_data['sources']:
    print(f"{source['name']} - {source['description']}")
