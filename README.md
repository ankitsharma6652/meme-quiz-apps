# 😂 MemeMaster - Viral Meme Discovery Platform

> Discover the hottest viral memes from across the internet!

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://ankitsharma6652.pythonanywhere.com)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.1.2-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

## 🌟 Live Demo

**Visit**: [https://ankitsharma6652.pythonanywhere.com](https://ankitsharma6652.pythonanywhere.com)

## ✨ Features

### 🎯 Core Features
- **Multi-Source Meme Fetching** - Aggregates memes from Reddit, Instagram, Twitter, 9GAG, TikTok, and YouTube
- **Smart Filtering** - Filter by media type (Images/Videos) and sort by Hot/Top/New
- **Infinite Scroll** - Load more memes seamlessly
- **Google OAuth Login** - Secure authentication with Google
- **Save Favorites** - Bookmark your favorite memes to your account
- **Download & Share** - Download memes or share them with friends
- **State Persistence** - Remembers your scroll position and filters on refresh

### 🎨 UI/UX
- **Modern Dark Theme** - Beautiful gradient design with glassmorphism effects
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Smooth Animations** - Polished micro-interactions
- **Video Playback** - Custom video player with controls
- **Lazy Loading** - Optimized image loading for better performance

### 🔐 User Features
- **User Profiles** - Track your favorite memes
- **Login History** - See when and where you logged in
- **Secure Sessions** - Flask-Login with session management

## 🚀 Tech Stack

### Backend
- **Framework**: Flask 3.1.2
- **Database**: MySQL (Production) / SQLite (Local)
- **Authentication**: Google OAuth 2.0 via Authlib
- **ORM**: Flask-SQLAlchemy
- **Server**: Gunicorn

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styling with gradients and animations
- **JavaScript** - Vanilla JS (no frameworks)
- **Fonts**: Google Fonts (Outfit)

### Deployment
- **Hosting**: PythonAnywhere (Free Tier)
- **CI/CD**: GitHub Actions (Auto-deploy)
- **Database**: MySQL on PythonAnywhere

## 📦 Installation

### Prerequisites
- Python 3.11+
- pip
- Git

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/ankitsharma6652/meme-quiz-apps.git
cd meme-quiz-apps
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file:
```env
SECRET_KEY=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

5. **Initialize database**
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

6. **Run the app**
```bash
python app.py
```

Visit: http://localhost:5000

## 🔧 Configuration

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI:
   - Local: `http://localhost:5000/authorize/google`
   - Production: `https://ankitsharma6652.pythonanywhere.com/authorize/google`
6. Copy Client ID and Client Secret to `.env`

### Database Configuration

The app automatically detects the environment:
- **Local**: Uses SQLite (`mememaster.db`)
- **PythonAnywhere**: Uses MySQL
- **Heroku/Render**: Uses PostgreSQL (if `DATABASE_URL` is set)

## 📁 Project Structure

```
meme-quiz-app/
├── app.py                      # Main Flask application
├── index.html                  # Frontend UI
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment config
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD
├── deploy.py                   # Deployment script
├── view_database.py            # Database viewer
├── check_db_connection.py      # DB connection checker
├── migrate_to_mysql.py         # MySQL migration script
├── init_db.py                  # Database initialization
├── PRODUCTION_SUMMARY.md       # Production documentation
├── PYTHONANYWHERE_GUIDE.md     # Deployment guide
├── DATABASE_ACCESS_GUIDE.md    # Database guide
└── MYSQL_SETUP_GUIDE.md        # MySQL setup guide
```

## 🗄️ Database Schema

### Tables

**user**
- `email` (PK) - User email
- `name` - User display name
- `picture` - Profile picture URL
- `created_at` - Account creation timestamp

**favorite**
- `id` (PK) - Favorite ID
- `user_email` (FK) - Reference to user
- `meme_id` - Unique meme identifier
- `meme_title` - Meme title
- `meme_url` - Meme URL
- `is_video` - Boolean flag
- `source` - Meme source platform
- `saved_at` - Timestamp

**login_history**
- `id` (PK) - Login record ID
- `user_email` (FK) - Reference to user
- `login_time` - Login timestamp
- `ip_address` - User IP address
- `user_agent` - Browser/device info
- `login_method` - Authentication method

## 🚀 Deployment

### PythonAnywhere (Current)

The app is deployed on PythonAnywhere with auto-deployment via GitHub Actions.

**Every push to `main` branch automatically deploys!**

```bash
git add .
git commit -m "Your changes"
git push origin main
```

See `PYTHONANYWHERE_GUIDE.md` for detailed setup instructions.

### Manual Deployment

If auto-deploy fails, manually reload on PythonAnywhere:
1. Go to Web tab
2. Click "Reload" button

## 📊 API Endpoints

### Public Endpoints
- `GET /` - Home page
- `GET /api/memes` - Fetch memes from all sources

### Authentication
- `GET /login/google` - Initiate Google OAuth
- `GET /authorize/google` - OAuth callback
- `GET /logout` - Logout user
- `GET /api/user` - Get current user info

### Protected Endpoints (Require Login)
- `GET /api/favorites` - Get user's favorites
- `POST /api/favorites` - Add favorite
- `DELETE /api/favorites/<meme_id>` - Remove favorite

## 🎨 Customization

### Changing Theme Colors

Edit the CSS variables in `index.html`:
```css
:root {
    --primary: #ff00cc;
    --secondary: #333399;
    --bg-dark: #0a0a0f;
    --card-bg: #1a1a1f;
}
```

### Adding New Meme Sources

Edit `app.py` and add your source to `get_memes()`:
```python
def fetch_your_source():
    # Your implementation
    return memes

# Add to get_memes()
executor.submit(fetch_your_source): 'YourSource'
```

## 🐛 Troubleshooting

### Videos Don't Have Audio
Most free meme APIs source from Reddit, which separates video and audio. Use the "Images Only" filter for best experience.

### OAuth Errors
1. Check redirect URIs in Google Console
2. Verify environment variables are set
3. Ensure using HTTPS in production

### Database Connection Issues
Run the diagnostic script:
```bash
python check_db_connection.py
```

## 📈 Performance

- **Parallel Fetching**: Fetches from 6 sources simultaneously
- **Lazy Loading**: Images load as you scroll
- **State Caching**: Remembers your position on refresh
- **Optimized Queries**: Database indexes for fast lookups

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Ankit Sharma**
- GitHub: [@ankitsharma6652](https://github.com/ankitsharma6652)
- Live App: [MemeMaster](https://ankitsharma6652.pythonanywhere.com)

## 🙏 Acknowledgments

- Meme sources: Reddit, Instagram, Twitter, 9GAG, TikTok, YouTube
- Icons: Emoji
- Fonts: Google Fonts (Outfit)
- Hosting: PythonAnywhere

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation files in the repo

---

**⭐ If you like this project, please give it a star!**

**🔗 Live Demo**: [https://ankitsharma6652.pythonanywhere.com](https://ankitsharma6652.pythonanywhere.com)
