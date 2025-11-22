# Deploy MemeMaster to Netlify + Supabase (100% Free, No Credit Card)

## 🎯 Overview

This setup uses:
- **Netlify**: Free hosting for your Flask app
- **Supabase**: Free PostgreSQL database
- **Result**: `https://mememaster.netlify.app`

**Total Cost**: $0 (Forever Free!)

---

## Part 1: Set Up Supabase Database (5 minutes)

### Step 1: Create Supabase Account
1. Go to https://supabase.com
2. Click **"Start your project"**
3. Sign up with **GitHub** (no credit card needed!)

### Step 2: Create New Project
1. Click **"New Project"**
2. Fill in:
   - **Name**: `mememaster`
   - **Database Password**: Create a strong password (save it!)
   - **Region**: Choose closest to you
3. Click **"Create new project"**
4. Wait 2-3 minutes for setup

### Step 3: Get Database Connection String
1. In your project dashboard, click **"Settings"** (gear icon)
2. Click **"Database"** in left sidebar
3. Scroll to **"Connection string"**
4. Select **"URI"** tab
5. Copy the connection string (looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
   ```
6. Replace `[YOUR-PASSWORD]` with your actual password
7. **Save this** - you'll need it!

---

## Part 2: Deploy to Netlify (5 minutes)

### Step 1: Create Netlify Account
1. Go to https://netlify.com
2. Click **"Sign up"**
3. Sign up with **GitHub** (no credit card needed!)

### Step 2: Deploy from GitHub
1. After login, click **"Add new site"** → **"Import an existing project"**
2. Click **"Deploy with GitHub"**
3. Authorize Netlify to access your GitHub
4. Select repository: `ankitsharma6652/meme-quiz-apps`
5. Configure build settings:
   - **Build command**: Leave empty
   - **Publish directory**: `.`
6. Click **"Deploy site"**

### Step 3: Configure Environment Variables
1. After deployment, go to **"Site settings"**
2. Click **"Environment variables"** in left sidebar
3. Click **"Add a variable"** and add these:

| Key | Value | Where to Get |
|-----|-------|--------------|
| `DATABASE_URL` | Your Supabase connection string | From Part 1, Step 3 |
| `GOOGLE_CLIENT_ID` | Your Google OAuth Client ID | Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | Your Google OAuth Client Secret | Google Cloud Console |
| `SECRET_KEY` | Any random 32+ character string | Generate with: `openssl rand -hex 32` |

4. Click **"Save"**

### Step 4: Change Site Name (Optional)
1. Go to **"Site settings"** → **"General"** → **"Site details"**
2. Click **"Change site name"**
3. Enter: `mememaster` (or `mememaster-app` if taken)
4. Click **"Save"**

Your URL will be: `https://mememaster.netlify.app`

### Step 5: Trigger Redeploy
1. Go to **"Deploys"** tab
2. Click **"Trigger deploy"** → **"Deploy site"**
3. Wait 2-3 minutes

---

## Part 3: Initialize Database

### Option A: Using Supabase SQL Editor (Easiest)
1. Go to your Supabase project
2. Click **"SQL Editor"** in left sidebar
3. Click **"New query"**
4. Paste this SQL:
```sql
-- Create users table
CREATE TABLE IF NOT EXISTS "user" (
    email VARCHAR(120) PRIMARY KEY,
    name VARCHAR(120),
    picture VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create favorites table
CREATE TABLE IF NOT EXISTS favorite (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(120) NOT NULL REFERENCES "user"(email) ON DELETE CASCADE,
    meme_id VARCHAR(200) NOT NULL,
    meme_title VARCHAR(500),
    meme_url VARCHAR(1000),
    is_video BOOLEAN DEFAULT FALSE,
    source VARCHAR(50),
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create login_history table
CREATE TABLE IF NOT EXISTS login_history (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(120) NOT NULL REFERENCES "user"(email) ON DELETE CASCADE,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    login_method VARCHAR(50) DEFAULT 'google'
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_favorite_user_email ON favorite(user_email);
CREATE INDEX IF NOT EXISTS idx_login_history_user_email ON login_history(user_email);
CREATE INDEX IF NOT EXISTS idx_login_history_login_time ON login_history(login_time);
```
5. Click **"Run"**
6. You should see "Success. No rows returned"

---

## Part 4: Update Google OAuth

1. Go to https://console.cloud.google.com/
2. Select your project
3. Go to **"Credentials"**
4. Click on your OAuth 2.0 Client ID
5. Add to **"Authorized redirect URIs"**:
   ```
   https://mememaster.netlify.app/authorize/google
   ```
   (Replace `mememaster` with your actual site name)
6. Click **"Save"**

---

## 🎉 You're Live!

Your app is now live at: **`https://mememaster.netlify.app`**

## 📊 Monitoring

### Netlify Dashboard
- **Deploys**: See deployment history and logs
- **Functions**: Monitor serverless function calls
- **Analytics**: View traffic stats (free tier)

### Supabase Dashboard
- **Table Editor**: View and edit database data
- **SQL Editor**: Run custom queries
- **Logs**: See database activity

## 🔄 Auto-Deploy

Every time you push to GitHub, Netlify automatically deploys!

```bash
git add .
git commit -m "Your changes"
git push origin main
```

## ⚡ Performance

**Free Tier Benefits:**
- ✅ No cold starts (always on!)
- ✅ Global CDN
- ✅ Automatic HTTPS
- ✅ 100GB bandwidth/month
- ✅ Unlimited deployments

## 🆙 Limits (Free Tier)

- **Netlify**: 
  - 100GB bandwidth/month
  - 300 build minutes/month
  - 125k serverless function requests/month

- **Supabase**:
  - 500MB database storage
  - 2GB bandwidth/month
  - 50,000 monthly active users

(More than enough for a meme app!)

## 🐛 Troubleshooting

### Deployment Failed?
1. Check **"Deploys"** → **"Deploy log"** for errors
2. Make sure all environment variables are set
3. Try triggering a new deploy

### Database Connection Error?
1. Verify `DATABASE_URL` is correct
2. Make sure you replaced `[YOUR-PASSWORD]` with actual password
3. Check Supabase project is running

### OAuth Not Working?
1. Verify redirect URI in Google Console
2. Check environment variables are set
3. Make sure using HTTPS (Netlify provides automatically)

## 📱 Your URLs

- **Live App**: `https://mememaster.netlify.app`
- **Netlify Dashboard**: `https://app.netlify.com`
- **Supabase Dashboard**: `https://app.supabase.com`

## 🎯 Advantages Over Other Hosts

✅ **No credit card required**
✅ **No cold starts** (unlike Render/Heroku free tier)
✅ **Global CDN** (faster than PythonAnywhere)
✅ **Better free limits** than most competitors
✅ **Professional URL** (netlify.app)
✅ **Auto-deploy** from GitHub
✅ **Free SSL** certificate

---

**Need help?** 
- Netlify Docs: https://docs.netlify.com
- Supabase Docs: https://supabase.com/docs
