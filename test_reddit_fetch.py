import requests
import json

def test_fetch():
    indian_subreddits = [
        'IndianDankMemes', 'IndiaMemes', 'SaimanSays', 'DesiMemes', 
        'bakchodi', 'IndianMeyMeys', 'bollywoodmemes', 'Chodi'
    ]
    
    headers = {'User-Agent': 'MemeQuizApp/1.0'}
    
    print(f"{'Subreddit':<20} | {'Status':<10} | {'Total':<5} | {'Images':<6} | {'Videos':<6} | {'NSFW':<5}")
    print("-" * 70)
    
    for sub in indian_subreddits:
        try:
            url = f'https://www.reddit.com/r/{sub}/hot.json?limit=20'
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code != 200:
                print(f"{sub:<20} | {response.status_code:<10} | {'-':<5} | {'-':<6} | {'-':<6} | {'-':<5}")
                continue
                
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            total = len(posts)
            images = 0
            videos = 0
            nsfw = 0
            
            for post in posts:
                p = post.get('data', {})
                if p.get('over_18'):
                    nsfw += 1
                
                if p.get('is_video'):
                    videos += 1
                elif p.get('url', '').endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    images += 1
            
            print(f"{sub:<20} | {response.status_code:<10} | {total:<5} | {images:<6} | {videos:<6} | {nsfw:<5}")
            
        except Exception as e:
            print(f"{sub:<20} | Error: {e}")

if __name__ == "__main__":
    test_fetch()
