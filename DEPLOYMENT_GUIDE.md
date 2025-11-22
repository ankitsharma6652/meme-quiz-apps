# MemeMaster - Deployment Guide

## ✅ Features Implemented:
1. **User Authentication** (Register/Login/Logout)
2. **SQLite Database** for user data and favorites
3. **Favorites System** - Save your favorite memes
4. **Secure password hashing** with bcrypt

## 🚀 Deploy to Render.com (FREE):

### Step 1: Prepare for Deployment
```bash
# Create a Procfile
echo "web: gunicorn app:app" > Procfile

# Create runtime.txt (optional)
echo "python-3.9.18" > runtime.txt
```

### Step 2: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - MemeMaster app"
# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/mememaster.git
git push -u origin main
```

### Step 3: Deploy on Render
1. Go to https://render.com
2. Sign up/Login (free account)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: mememaster
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free
6. Add Environment Variable:
   - Key: `SECRET_KEY`
   - Value: (generate a random string)
7. Click "Create Web Service"

Your app will be live at: `https://mememaster.onrender.com`

## 🔐 Database Access:

The SQLite database file `mememaster.db` will be created automatically.

### Admin Access:
To access the database, you can:
1. SSH into Render (paid plan) OR
2. Add an admin route to view users (I can add this)

### Database Schema:
**Users Table:**
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- created_at

**Favorites Table:**
- id (Primary Key)
- user_id (Foreign Key → Users)
- meme_id
- meme_title
- meme_url
- is_video
- source
- saved_at

## 📡 API Endpoints:

### Authentication:
- `POST /api/register` - Register new user
- `POST /api/login` - Login
- `POST /api/logout` - Logout
- `GET /api/current-user` - Get current user info

### Favorites:
- `GET /api/favorites` - Get user's favorites
- `POST /api/favorites` - Add to favorites
- `DELETE /api/favorites/<id>` - Remove from favorites

### Memes:
- `GET /api/trending-memes` - Get trending memes

## 🎨 Frontend Integration Needed:

The backend is ready! You need to add UI for:
1. Login/Register forms
2. Logout button
3. "Add to Favorites" button on each meme
4. "My Favorites" page

I can create this UI if you want!

## 🔧 Local Testing:

```bash
python3 app.py
```

Visit: http://localhost:5000

## 📊 View Database (Local):

```bash
sqlite3 mememaster.db
.tables
SELECT * FROM user;
SELECT * FROM favorite;
.quit
```

## 🌐 Alternative Free Hosting Options:

1. **Render.com** (Recommended) - Free tier, auto-deploy from Git
2. **Railway.app** - $5 free credit monthly
3. **Fly.io** - Free tier available
4. **PythonAnywhere** - Free tier with limitations

## 🔐 Your Admin Credentials:

After deployment, register the first account - that will be yours!

Username: (you choose)
Email: (you choose)
Password: (you choose)

## 📝 Next Steps:

1. Would you like me to create the login/register UI?
2. Should I add an admin panel to view all users?
3. Do you want to deploy now or test locally first?

Let me know and I'll help you with the next step!
