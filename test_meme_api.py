import requests
import json

print("🕵️‍♂️ Testing Meme-API for Videos...")

subs = ['DesiVideoMemes', 'IndianDankMemes']
video_count = 0

for sub in subs:
    url = f"https://meme-api.com/gimme/{sub}/50"
    try:
        r = requests.get(url)
        data = r.json()
        memes = data.get('memes', [])
        
        print(f"\nChecked r/{sub}: {len(memes)} posts")
        
        for meme in memes:
            url = meme.get('url', '')
            # Check for video extensions or domains
            if url.endswith('.mp4') or 'v.redd.it' in url or 'gfycat' in url:
                print(f"   🎥 FOUND VIDEO: {url}")
                video_count += 1
            
    except Exception as e:
        print(f"Error: {e}")

print(f"\nTotal Videos Found: {video_count}")
