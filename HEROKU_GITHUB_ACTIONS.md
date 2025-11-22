# Automated Heroku Deployment via GitHub Actions

This guide will help you set up automatic deployment to Heroku whenever you push to GitHub.

## Prerequisites

1. **Heroku Account** - Sign up at https://heroku.com (free)
2. **GitHub Repository** - Your code is already on GitHub ✅

## Step 1: Create Heroku App (One-time setup)

### Option A: Via Heroku Dashboard (Easiest)
1. Go to https://dashboard.heroku.com/apps
2. Click **"New"** → **"Create new app"**
3. Enter app name: `mememaster` (or `mememaster-app` if taken)
4. Choose region: **United States** or **Europe**
5. Click **"Create app"**

### Option B: Via Heroku CLI (if you have it)
```bash
heroku create mememaster
```

## Step 2: Add PostgreSQL Database

1. In your Heroku app dashboard, go to **"Resources"** tab
2. In "Add-ons" search box, type: `Heroku Postgres`
3. Select **"Heroku Postgres"**
4. Choose plan: **"Mini"** (Free)
5. Click **"Submit Order Form"**

## Step 3: Get Your Heroku API Key

1. Go to https://dashboard.heroku.com/account
2. Scroll down to **"API Key"**
3. Click **"Reveal"**
4. **Copy the API key** (you'll need this for GitHub)

## Step 4: Configure GitHub Secrets

1. Go to your GitHub repository: https://github.com/ankitsharma6652/meme-quiz-apps
2. Click **"Settings"** tab
3. In left sidebar, click **"Secrets and variables"** → **"Actions"**
4. Click **"New repository secret"** and add these **3 secrets**:

### Secret 1: HEROKU_API_KEY
- **Name**: `HEROKU_API_KEY`
- **Value**: Paste your Heroku API key from Step 3
- Click **"Add secret"**

### Secret 2: HEROKU_APP_NAME
- **Name**: `HEROKU_APP_NAME`
- **Value**: `mememaster` (or whatever name you chose)
- Click **"Add secret"**

### Secret 3: HEROKU_EMAIL
- **Name**: `HEROKU_EMAIL`
- **Value**: Your Heroku account email
- Click **"Add secret"**

### Secret 4: GOOGLE_CLIENT_ID (for OAuth)
- **Name**: `GOOGLE_CLIENT_ID`
- **Value**: Your Google OAuth Client ID
- Click **"Add secret"**

### Secret 5: GOOGLE_CLIENT_SECRET (for OAuth)
- **Name**: `GOOGLE_CLIENT_SECRET`
- **Value**: Your Google OAuth Client Secret
- Click **"Add secret"**

## Step 5: Set Heroku Environment Variables

1. Go to your Heroku app dashboard
2. Click **"Settings"** tab
3. Click **"Reveal Config Vars"**
4. Add these config vars:

| Key | Value |
|-----|-------|
| `GOOGLE_CLIENT_ID` | Your Google OAuth Client ID |
| `GOOGLE_CLIENT_SECRET` | Your Google OAuth Client Secret |
| `SECRET_KEY` | Generate with: `openssl rand -hex 32` |

**Note**: `DATABASE_URL` is automatically added by Heroku Postgres addon.

## Step 6: Update Google OAuth Redirect URI

1. Go to https://console.cloud.google.com/
2. Select your project
3. Go to **"Credentials"**
4. Click on your OAuth 2.0 Client ID
5. Add to **"Authorized redirect URIs"**:
   ```
   https://mememaster.herokuapp.com/authorize/google
   ```
   (Replace `mememaster` with your actual app name)
6. Click **"Save"**

## Step 7: Deploy! 🚀

Now, every time you push to GitHub, it will automatically deploy to Heroku!

```bash
git add .
git commit -m "Setup automated Heroku deployment"
git push origin main
```

## Step 8: Monitor Deployment

1. Go to your GitHub repository
2. Click **"Actions"** tab
3. You'll see the deployment running
4. Wait for the green checkmark ✅

## Step 9: Initialize Database (First time only)

After first deployment, run this once:

### Via Heroku Dashboard
1. Go to your app dashboard
2. Click **"More"** → **"Run console"**
3. Type: `python`
4. Click **"Run"**
5. In the console, paste:
```python
from app import app, db
app.app_context().push()
db.create_all()
print("Database initialized!")
```

### Via Heroku CLI (if you have it)
```bash
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## Your App URLs

- **Heroku App**: `https://mememaster.herokuapp.com`
- **Heroku Dashboard**: `https://dashboard.heroku.com/apps/mememaster`
- **GitHub Actions**: `https://github.com/ankitsharma6652/meme-quiz-apps/actions`

## Troubleshooting

### Check Deployment Logs
1. Go to Heroku dashboard
2. Click **"More"** → **"View logs"**

### Check GitHub Actions Logs
1. Go to GitHub repository
2. Click **"Actions"** tab
3. Click on the latest workflow run
4. Click on **"deploy"** job to see logs

### Common Issues

**Issue**: Deployment fails with "App not found"
- **Solution**: Make sure `HEROKU_APP_NAME` secret matches your actual Heroku app name

**Issue**: Database errors
- **Solution**: Make sure PostgreSQL addon is added and run database initialization

**Issue**: OAuth errors
- **Solution**: Check that redirect URI is added in Google Console and config vars are set

## Future Deployments

From now on, just push to GitHub and it deploys automatically:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

That's it! Your app will be live at `https://mememaster.herokuapp.com` 🎉
