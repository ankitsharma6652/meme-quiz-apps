import requests
import json
import sys

print("="*60)
print("🕵️‍♂️ REDDIT FETCH DIAGNOSTIC")
print("="*60)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

subs = ['DesiVideoMemes', 'IndianDankMemes']

for sub in subs:
    url = f'https://www.reddit.com/r/{sub}/hot.json?limit=5'
    print(f"\n1. Fetching r/{sub}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            print(f"   Posts Found: {len(posts)}")
            
            video_count = 0
            for post in posts:
                p = post.get('data', {})
                if p.get('is_video'):
                    video_count += 1
                    print(f"   ✅ Found Video: {p.get('title')[:30]}...")
            
            if video_count == 0:
                print("   ⚠️ No videos found in top 5 posts (might be all images/text)")
        elif response.status_code == 429:
            print("   ❌ RATE LIMITED (429) - Reddit is blocking us.")
        elif response.status_code == 403:
            print("   ❌ FORBIDDEN (403) - Reddit blocked the IP/User-Agent.")
        else:
            print(f"   ❌ Error: {response.text[:100]}")
            
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")

print("\n" + "="*60)
