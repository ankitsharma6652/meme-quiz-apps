# 🎭 MemeMaster - Trending Meme Feed

A modern web application that displays trending memes from Reddit and other sources, with Google Sign-In authentication and a favorites system.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🔐 **Google OAuth Authentication** - Secure sign-in with your Google account
- 🎨 **Modern UI** - Beautiful, responsive design with glassmorphism effects
- ❤️ **Favorites System** - Save your favorite memes for later
- 🔄 **Real-time Meme Feed** - Fetches trending memes from Reddit and Meme API
- 📱 **Responsive Design** - Works perfectly on desktop and mobile
- 🎯 **Filter & Sort** - Filter by media type and sort by popularity
- 💾 **Persistent Data** - SQLite database stores user data and favorites

## 🚀 Live Demo

Visit the live app: [Your PythonAnywhere URL]

## 📸 Screenshots

[Add screenshots of your app here]

## 🛠️ Tech Stack

**Backend:**
- Flask (Python web framework)
- SQLAlchemy (Database ORM)
- Authlib (OAuth 2.0 implementation)
- SQLite (Database)

**Frontend:**
- HTML5
- CSS3 (with modern animations)
- Vanilla JavaScript

**APIs:**
- Google OAuth 2.0 API
- Reddit JSON API
- Meme API (meme-api.com)

## 📋 Prerequisites

- Python 3.9 or higher
- Google Cloud Console account (for OAuth credentials)
- Git

## 🔧 Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/ankitsharma6652/meme-quiz-apps.git
cd meme-quiz-apps
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:5000/authorize/google`
6. Copy Client ID and Client Secret

### 5. Create `.env` file

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 6. Run the application

```bash
python3 app.py
```

Visit `http://localhost:5000` in your browser.

## 🌐 Deployment

### Deploy to PythonAnywhere (FREE)

Detailed deployment guide available in [`PYTHONANYWHERE_GUIDE.md`](PYTHONANYWHERE_GUIDE.md)

**Quick steps:**
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Clone your repository in Bash console
3. Configure WSGI file with environment variables
4. Update Google OAuth redirect URI
5. Reload web app

### Deploy to Render.com

See [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) for Render deployment instructions.

## 📁 Project Structure

```
meme-quiz-apps/
├── app.py                      # Main Flask application
├── index.html                  # Frontend UI
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment configuration
├── .gitignore                  # Git ignore rules
├── .env                        # Environment variables (not in git)
├── instance/
│   └── mememaster.db          # SQLite database
├── PYTHONANYWHERE_GUIDE.md    # PythonAnywhere deployment guide
├── DEPLOYMENT_GUIDE.md        # Render deployment guide
└── README.md                  # This file
```

## 🗄️ Database Schema

**Users Table:**
- `id` - Primary key
- `email` - User's email (from Google)
- `name` - User's name (from Google)
- `picture` - Profile picture URL
- `created_at` - Account creation timestamp

**Favorites Table:**
- `id` - Primary key
- `user_id` - Foreign key to Users
- `meme_id` - Unique meme identifier
- `meme_title` - Meme title
- `meme_url` - Meme image/video URL
- `is_video` - Boolean flag
- `source` - Source platform (Reddit, Meme API, etc.)
- `saved_at` - Timestamp when favorited

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask session secret key | Yes |
| `GOOGLE_CLIENT_ID` | Google OAuth Client ID | Yes |
| `GOOGLE_CLIENT_SECRET` | Google OAuth Client Secret | Yes |
| `AUTHLIB_INSECURE_TRANSPORT` | Allow HTTP for localhost (set to `1`) | Development only |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Ankit Sharma**
- GitHub: [@ankitsharma6652](https://github.com/ankitsharma6652)

## 🙏 Acknowledgments

- [Reddit](https://www.reddit.com) for the meme content API
- [Meme API](https://meme-api.com) for additional meme sources
- [Google](https://developers.google.com) for OAuth 2.0 services
- [Flask](https://flask.palletsprojects.com/) for the awesome web framework

## 📞 Support

If you have any questions or run into issues, please open an issue on GitHub.

---

⭐ **Star this repo if you found it helpful!** ⭐
