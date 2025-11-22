"""
Check favorites in the database
"""
import os
import sys

# Set environment to use PythonAnywhere MySQL
os.environ['PYTHONANYWHERE_DOMAIN'] = 'ankitsharma6652.pythonanywhere.com'

from app import app, db, Favorite, User

with app.app_context():
    print("=" * 60)
    print("CHECKING FAVORITES IN DATABASE")
    print("=" * 60)
    
    # Get all users
    users = User.query.all()
    print(f"\nTotal users: {len(users)}")
    
    for user in users:
        print(f"\n📧 User: {user.email}")
        print(f"   Name: {user.name}")
        
        # Get favorites for this user
        favorites = Favorite.query.filter_by(user_email=user.email).all()
        print(f"   Favorites: {len(favorites)}")
        
        if favorites:
            print("\n   Saved memes:")
            for i, fav in enumerate(favorites, 1):
                print(f"\n   {i}. ID: {fav.id}")
                print(f"      Meme ID: {fav.meme_id}")
                print(f"      Title: {fav.meme_title}")
                print(f"      URL: {fav.meme_url[:80]}..." if len(fav.meme_url) > 80 else f"      URL: {fav.meme_url}")
                print(f"      Is Video: {fav.is_video}")
                print(f"      Source: {fav.source}")
                print(f"      Saved: {fav.saved_at}")
                
                # Check if URL is accessible
                import requests
                try:
                    r = requests.head(fav.meme_url, timeout=5, allow_redirects=True)
                    if r.status_code == 200:
                        print(f"      ✅ URL is accessible")
                    else:
                        print(f"      ❌ URL returns {r.status_code}")
                except Exception as e:
                    print(f"      ❌ URL is broken: {str(e)[:50]}")
    
    print("\n" + "=" * 60)
