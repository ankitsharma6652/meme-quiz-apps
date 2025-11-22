"""
Test script to verify all API routes are accessible
"""
import requests

BASE_URL = "https://ankitsharma6652.pythonanywhere.com"

def test_routes():
    print("Testing API routes...\n")
    
    # Test GET /api/memes
    print("1. Testing GET /api/memes")
    try:
        r = requests.get(f"{BASE_URL}/api/memes", timeout=10)
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"   ✅ Success - Got {len(data)} memes")
        else:
            print(f"   ❌ Failed - {r.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test GET /api/favorites (should return 401 without auth)
    print("2. Testing GET /api/favorites (without auth)")
    try:
        r = requests.get(f"{BASE_URL}/api/favorites", timeout=10)
        print(f"   Status: {r.status_code}")
        if r.status_code == 401:
            print(f"   ✅ Correct - Returns 401 Unauthorized")
        else:
            print(f"   Response: {r.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test POST /api/favorites (should return 401 without auth)
    print("3. Testing POST /api/favorites (without auth)")
    try:
        r = requests.post(
            f"{BASE_URL}/api/favorites",
            json={"meme_id": "test", "title": "Test", "url": "http://test.com"},
            timeout=10
        )
        print(f"   Status: {r.status_code}")
        if r.status_code == 401:
            print(f"   ✅ Correct - Returns 401 Unauthorized")
        elif r.status_code == 404:
            print(f"   ❌ PROBLEM - Route not found! App needs reload.")
        else:
            print(f"   Response: {r.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 50)
    print("If POST /api/favorites returns 404:")
    print("1. Go to: https://www.pythonanywhere.com/user/ankitsharma6652/webapps/")
    print("2. Click the 'Reload' button")
    print("3. Run this test again")
    print("=" * 50)

if __name__ == "__main__":
    test_routes()
