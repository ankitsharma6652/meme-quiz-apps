# Heroku Deployment Guide for MemeMaster

## Prerequisites
1. Create a free Heroku account at https://heroku.com
2. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

## Step 1: Login to Heroku
```bash
heroku login
```

## Step 2: Create Heroku App
```bash
# Create app with your desired name
heroku create mememaster

# Or if 'mememaster' is taken, try variations:
# heroku create mememaster-app
# heroku create mememaster-viral
# heroku create mememaster-memes
```

## Step 3: Add PostgreSQL Database (Free)
```bash
heroku addons:create heroku-postgresql:mini
```

## Step 4: Set Environment Variables
```bash
# Set your Google OAuth credentials
heroku config:set GOOGLE_CLIENT_ID="your_google_client_id"
heroku config:set GOOGLE_CLIENT_SECRET="your_google_client_secret"

# Set secret key
heroku config:set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"

# Set production flag
heroku config:set PRODUCTION=true
```

## Step 5: Update app.py for PostgreSQL
The app is already configured to use PostgreSQL on Heroku!
It will automatically detect the `DATABASE_URL` environment variable.

## Step 6: Deploy
```bash
# Add Heroku remote (if not already added)
heroku git:remote -a mememaster

# Push to Heroku
git push heroku main

# Open your app
heroku open
```

## Step 7: Initialize Database
```bash
# Run database migrations
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## Monitoring & Logs
```bash
# View logs
heroku logs --tail

# Check app status
heroku ps

# Restart app
heroku restart
```

## Your App URLs
- Main app: `https://mememaster.herokuapp.com` (or your chosen name)
- Heroku dashboard: `https://dashboard.heroku.com/apps/mememaster`

## Updating Your App
Whenever you make changes:
```bash
git add .
git commit -m "Your update message"
git push heroku main
```

## Free Tier Limits
- 550 dyno hours/month (enough for 24/7 if you verify your account with a credit card)
- 10,000 rows in PostgreSQL
- App sleeps after 30 min of inactivity (wakes up on first request)

## Troubleshooting
If deployment fails:
```bash
# Check build logs
heroku logs --tail

# Check config
heroku config

# Restart
heroku restart
```
