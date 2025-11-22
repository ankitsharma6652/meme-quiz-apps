import cloudscraper
import json
import sys

print("="*60)
print("🛡️ REDDIT BYPASS TEST (CloudScraper)")
print("="*60)

# Create a scraper instance
scraper = cloudscraper.create_scraper()

subs = ['DesiVideoMemes', 'IndianDankMemes']

for sub in subs:
    url = f'https://www.reddit.com/r/{sub}/hot.json?limit=5'
    print(f"\n1. Fetching r/{sub}...")
    try:
        response = scraper.get(url)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            print(f"   ✅ SUCCESS! Found {len(posts)} posts.")
            
            video_count = 0
            for post in posts:
                p = post.get('data', {})
                if p.get('is_video'):
                    video_count += 1
                    print(f"      🎥 Video: {p.get('title')[:30]}...")
            
            if video_count == 0:
                print("      ⚠️ No videos in top 5.")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "="*60)
