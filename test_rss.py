import requests
import json
import urllib.parse

print("🕵️‍♂️ Testing RSS-to-JSON Strategy...")

# Reddit RSS URL
subreddit = "DesiVideoMemes"
rss_url = f"https://www.reddit.com/r/{subreddit}/hot.rss"
encoded_url = urllib.parse.quote(rss_url)

# Service 1: rss2json.com
api_url = f"https://api.rss2json.com/v1/api.json?rss_url={encoded_url}"

print(f"\n1. Fetching from: {api_url}")

try:
    response = requests.get(api_url)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        print(f"   ✅ Success! Found {len(items)} items.")
        
        for item in items[:3]:
            print(f"      - {item.get('title')}")
            print(f"        Link: {item.get('link')}")
            # RSS content usually contains the HTML, we'd need to parse it for video links
            content = item.get('content', '')
            print(f"        📄 Content Preview: {content[:500]}...")
            
            if 'video' in content or 'mp4' in content:
                print("        🎥 Potential Video Content Found")
    else:
        print(f"   ❌ Failed: {response.text}")

except Exception as e:
    print(f"   ❌ Error: {e}")
