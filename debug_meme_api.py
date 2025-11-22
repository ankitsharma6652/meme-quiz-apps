import requests
import json

print("🕵️‍♂️ Deep Inspection of Meme-API...")

# Fetch 50 posts from a video-only subreddit
url = "https://meme-api.com/gimme/DesiVideoMemes/50"
try:
    r = requests.get(url)
    data = r.json()
    memes = data.get('memes', [])
    
    print(f"Fetched {len(memes)} posts.")
    
    for i, meme in enumerate(memes[:10]): # Look at first 10
        print(f"\n[{i}] Title: {meme.get('title')}")
        print(f"    URL: {meme.get('url')}")
        print(f"    Post Link: {meme.get('postLink')}")
        
        # Check if it looks like a video
        if 'v.redd.it' in meme.get('url', '') or '.mp4' in meme.get('url', ''):
            print("    ✅ LOOKS LIKE A VIDEO!")
        else:
            print("    ❌ Looks like an image")

except Exception as e:
    print(f"Error: {e}")
