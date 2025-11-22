import requests
import json

print("🕵️‍♂️ Testing Serverless Reddit API...")

url = "https://sra.vercel.app/api/posts?subreddit=DesiVideoMemes"

try:
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        posts = data.get('data', [])
        print(f"✅ Success! Found {len(posts)} posts.")
        
        for post in posts[:3]:
            print(f"   - {post.get('title')}")
            if post.get('url'):
                print(f"     URL: {post.get('url')}")
    else:
        print(f"❌ Failed: {response.text}")

except Exception as e:
    print(f"❌ Error: {e}")
