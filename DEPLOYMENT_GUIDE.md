# MemeMaster - Deployment Guide

## ✅ Features Implemented:
1. **Google User Authentication** (Sign in with Google)
2. **SQLite Database** for user data and favorites
3. **Favorites System** - Save your favorite memes
4. **Token-based Authentication** for secure API access

## 🚀 Deploy to Render.com (FREE):

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/mememaster.git
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to [Render.com](https://render.com)
2. Sign up/Login (free account)
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - **Name**: mememaster
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free
6. **CRITICAL**: Add Environment Variables (Scroll down to "Environment Variables"):
   - `SECRET_KEY`: (generate a random string)
   - `GOOGLE_CLIENT_ID`: (paste from your .env file)
   - `GOOGLE_CLIENT_SECRET`: (paste from your .env file)
   - `AUTHLIB_INSECURE_TRANSPORT`: `1` (Optional, but good for testing)
7. Click **"Create Web Service"**

### ⚠️ Important Note on Database:
On Render's Free Tier, the **SQLite database will be reset** every time you deploy or if the server restarts (which happens automatically after inactivity).
- **For Hobby/Testing**: This is fine.
- **For Permanent Data**: You would need to upgrade to a paid plan or connect a free external database like **Neon (Postgres)** or **Supabase**.

## 🌐 Other Free Options:

1. **PythonAnywhere**:
   - **Pros**: Persistent SQLite database (data won't be lost).
   - **Cons**: Older interface, manual file upload or git pull.
   - **URL**: [pythonanywhere.com](https://www.pythonanywhere.com/)

2. **Railway.app**:
   - **Pros**: Great UI, persistent volumes.
   - **Cons**: Trial only (no permanent free tier).

## � Google Cloud Setup for Production:
When you deploy, your URL will change (e.g., `https://mememaster.onrender.com`).
You **MUST** add this new URL to your Google Cloud Console:
1. Go to Google Cloud Console > APIs & Services > Credentials.
2. Edit your OAuth Client.
3. Add to **Authorized Redirect URIs**:
   - `https://YOUR-APP-NAME.onrender.com/authorize/google`
4. Save.

## 📝 Next Steps:
1. Push code to GitHub.
2. Create Render service.
3. Update Google Console with new URL.
4. Enjoy! 🚀
