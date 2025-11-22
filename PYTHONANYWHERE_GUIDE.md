# PythonAnywhere Deployment Guide

## ✅ Why PythonAnywhere?
- **FREE forever** (no credit card needed)
- **Database persists** (your users and favorites won't be lost!)
- **Always-on** (no cold starts)

Your app will be at: `https://YOUR-USERNAME.pythonanywhere.com`

---

## 🚀 Step-by-Step Deployment

### Step 1: Create Account
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Click **"Pricing & signup"** → **"Create a Beginner account"**
3. Choose a username (e.g., `ankitsharma` → URL will be `ankitsharma.pythonanywhere.com`)
4. Verify your email

### Step 2: Upload Code via Git
1. On PythonAnywhere dashboard, click **"Consoles"** tab
2. Click **"Bash"** to open a terminal
3. Run these commands:

```bash
# Clone your repository (replace with your GitHub URL)
git clone https://github.com/YOUR-USERNAME/meme-quiz-app.git
cd meme-quiz-app

# Install dependencies
pip3.10 install --user -r requirements.txt
```

### Step 3: Create Web App
1. Click **"Web"** tab in the top menu
2. Click **"Add a new web app"**
3. Click **"Next"** (accept the domain name)
4. Select **"Manual configuration"**
5. Choose **"Python 3.10"**
6. Click **"Next"**

### Step 4: Configure WSGI File
1. Scroll down to **"Code"** section
2. Click on the **WSGI configuration file** link (e.g., `/var/www/username_pythonanywhere_com_wsgi.py`)
3. **Delete all content** and replace with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR-USERNAME/meme-quiz-app'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables
os.environ['SECRET_KEY'] = 'your-secret-key-from-env-file'
os.environ['GOOGLE_CLIENT_ID'] = 'your-google-client-id'
os.environ['GOOGLE_CLIENT_SECRET'] = 'your-google-client-secret'
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'

# Import Flask app
from app import app as application
```

4. **IMPORTANT**: Replace:
   - `YOUR-USERNAME` with your PythonAnywhere username
   - `your-secret-key-from-env-file` with the SECRET_KEY from your `.env` file
   - `your-google-client-id` with your GOOGLE_CLIENT_ID
   - `your-google-client-secret` with your GOOGLE_CLIENT_SECRET

5. Click **"Save"** (top right)

### Step 5: Set Working Directory
1. Go back to the **"Web"** tab
2. Scroll to **"Code"** section
3. Set **"Working directory"** to: `/home/YOUR-USERNAME/meme-quiz-app`
4. Set **"Source code"** to: `/home/YOUR-USERNAME/meme-quiz-app`

### Step 6: Configure Static Files
1. Scroll to **"Static files"** section
2. Click **"Enter URL"** and add:
   - URL: `/static/`
   - Directory: `/home/YOUR-USERNAME/meme-quiz-app/static`
3. (Optional, if you have static files)

### Step 7: Reload Web App
1. Scroll to the top of the **"Web"** tab
2. Click the big green **"Reload"** button
3. Wait 10 seconds

### Step 8: Update Google Cloud Console
Your app is now at: `https://YOUR-USERNAME.pythonanywhere.com`

**CRITICAL**: Update Google OAuth redirect URI:
1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Edit your OAuth 2.0 Client
3. Add to **Authorized redirect URIs**:
   ```
   https://YOUR-USERNAME.pythonanywhere.com/authorize/google
   ```
4. Click **"Save"**

### Step 9: Test!
1. Visit `https://YOUR-USERNAME.pythonanywhere.com`
2. Click **"Sign in with Google"**
3. You should be logged in! 🎉

---

## 🔧 Troubleshooting

### Error: "Something went wrong"
1. Click **"Web"** tab
2. Click **"Error log"** link
3. Read the error message
4. Common fixes:
   - Check WSGI file paths
   - Verify environment variables
   - Make sure `pip install` completed

### Error: "redirect_uri_mismatch"
- Make sure you added the **exact** URL to Google Console
- Format: `https://username.pythonanywhere.com/authorize/google`

### Database not working
1. Go to **"Files"** tab
2. Navigate to `/home/YOUR-USERNAME/meme-quiz-app/instance/`
3. Check if `mememaster.db` exists
4. If not, the app will create it on first login

---

## 🔄 Updating Your App

When you make changes:
1. Push to GitHub: `git push`
2. On PythonAnywhere Bash console:
   ```bash
   cd meme-quiz-app
   git pull
   ```
3. Click **"Reload"** on Web tab

---

## 📊 View Your Database

1. Go to **"Consoles"** → **"Bash"**
2. Run:
   ```bash
   cd meme-quiz-app/instance
   sqlite3 mememaster.db
   .tables
   SELECT * FROM user;
   .quit
   ```

---

## ✅ You're Done!

Your app is now live at: `https://YOUR-USERNAME.pythonanywhere.com`

Share it with friends! 🚀
