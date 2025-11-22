import requests
import json

def test_video_fetch():
    video_subs = ['DesiVideoMemes', 'IndianDankMemes', 'bollywoodmemes']
    headers = {'User-Agent': 'MemeQuizApp/1.0'}
    
    print(f"{'Subreddit':<20} | {'Status':<10} | {'Videos Found':<15}")
    print("-" * 60)
    
    for sub in video_subs:
        try:
            url = f'https://www.reddit.com/r/{sub}/hot.json?limit=25'
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code != 200:
                print(f"{sub:<20} | {response.status_code:<10} | -")
                continue
                
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            video_count = 0
            for post in posts:
                p = post.get('data', {})
                if p.get('is_video') and p.get('secure_media'):
                    video_data = p.get('secure_media', {}).get('reddit_video', {})
                    if video_data.get('fallback_url'):
                        video_count += 1
                        # Print first video URL as sample
                        if video_count == 1:
                            print(f"   Sample: {video_data.get('fallback_url')}")
            
            print(f"{sub:<20} | {response.status_code:<10} | {video_count:<15}")
            
        except Exception as e:
            print(f"{sub:<20} | Error: {e}")

if __name__ == "__main__":
    test_video_fetch()
