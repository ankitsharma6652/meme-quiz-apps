import os
import requests
import sys

# Configuration
USERNAME = os.environ.get('PA_USERNAME')
TOKEN = os.environ.get('PA_API_TOKEN')
DOMAIN = os.environ.get('PA_DOMAIN')
BASE_URL = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}"

if not all([USERNAME, TOKEN, DOMAIN]):
    print("❌ Missing environment variables (PA_USERNAME, PA_API_TOKEN, PA_DOMAIN)")
    sys.exit(1)

HEADERS = {'Authorization': f'Token {TOKEN}'}

def upload_file(local_path, remote_path):
    print(f"📤 Uploading {local_path} -> {remote_path}...")
    try:
        with open(local_path, 'rb') as f:
            files = {'content': f}
            response = requests.post(
                f"{BASE_URL}/files/path/home/{USERNAME}/meme-quiz-apps/{remote_path}",
                headers=HEADERS,
                files=files
            )
            if response.status_code in [200, 201]:
                print("   ✅ Success")
            else:
                print(f"   ❌ Failed: {response.status_code} - {response.text}")
                sys.exit(1)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        sys.exit(1)

def reload_webapp():
    print(f"🔄 Reloading {DOMAIN}...")
    response = requests.post(
        f"{BASE_URL}/webapps/{DOMAIN}/reload/",
        headers=HEADERS
    )
    if response.status_code == 200:
        print("   ✅ Web app reloaded!")
    else:
        print(f"   ❌ Reload failed: {response.status_code} - {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Starting Direct File Deployment...")
    
    # List of files to sync
    files_to_sync = [
        ('app.py', 'app.py'),
        ('templates/index.html', 'templates/index.html'),
        ('requirements.txt', 'requirements.txt'),
        ('verify_deployment.py', 'verify_deployment.py')
    ]
    
    for local, remote in files_to_sync:
        if os.path.exists(local):
            upload_file(local, remote)
        else:
            print(f"⚠️ Skipping missing file: {local}")
            
    reload_webapp()
    print("✨ Deployment Complete!")
