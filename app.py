from flask import Flask, request, jsonify, send_from_directory, Response, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import requests
import os
import html
import secrets
import random
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Allow OAuth over HTTP for localhost
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='', static_folder='.')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Database Configuration - Support multiple platforms
if os.environ.get('DATABASE_URL'):
    # Heroku: PostgreSQL
    database_url = os.environ.get('DATABASE_URL')
    # Heroku uses 'postgres://' but SQLAlchemy needs 'postgresql://'
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print("Using Heroku PostgreSQL database")
elif os.environ.get('PYTHONANYWHERE_DOMAIN'):
    # PythonAnywhere: MySQL
    from urllib.parse import quote_plus
    MYSQL_USER = os.environ.get('MYSQL_USER', 'ankitsharma6652')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'ankitsharma6652.mysql.pythonanywhere-services.com')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'ankitsharma6652$mememaster')
    
    encoded_password = quote_plus(MYSQL_PASSWORD)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}/{MYSQL_DB}'
    print(f"Using PythonAnywhere MySQL database: {MYSQL_DB}")
else:
    # Local: SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mememaster.db'
    print("Using SQLite database: mememaster.db")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 280,
    'pool_pre_ping': True,
}

# Session Configuration
app.config['SESSION_COOKIE_SECURE'] = True  # Require HTTPS in production
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400 # 1 day

# Force HTTPS in production (skip for localhost)
@app.before_request
def force_https():
    if request.headers.get('X-Forwarded-Proto') == 'http' and 'localhost' not in request.host and '127.0.0.1' not in request.host:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

# Google OAuth Configuration
# You MUST get these from Google Cloud Console: https://console.cloud.google.com/
app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET', 'YOUR_GOOGLE_CLIENT_SECRET')

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
oauth = OAuth(app)

# Configure Google OAuth
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs' # Add JWKS URI for better validation
)

# Database Models
class User(UserMixin, db.Model):
    email = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(120))
    picture = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    favorites = db.relationship('Favorite', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def get_id(self):
        return self.email

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    meme_id = db.Column(db.String(200), nullable=False)
    meme_title = db.Column(db.String(500))
    meme_url = db.Column(db.String(1000))
    is_video = db.Column(db.Boolean, default=False)
    source = db.Column(db.String(50))
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

class LoginHistory(db.Model):
    __tablename__ = 'login_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(
        db.String(120), 
        db.ForeignKey('user.email', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    login_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    ip_address = db.Column(db.String(45))  # IPv6 can be up to 45 chars
    user_agent = db.Column(db.String(500))
    login_method = db.Column(db.String(50), default='google')  # 'google', 'facebook', etc.

class UserMeme(db.Model):
    __tablename__ = 'user_memes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    title = db.Column(db.String(500))
    image_data = db.Column(db.Text, nullable=False)  # Base64 encoded image
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    upvotes = db.Column(db.Integer, default=0)
    
    user = db.relationship('User', backref='memes')

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    meme_id = db.Column(db.Integer, db.ForeignKey('user_memes.id'), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='comments')
    meme = db.relationship('UserMeme', backref='comments')

class Upvote(db.Model):
    __tablename__ = 'upvotes'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    meme_id = db.Column(db.Integer, db.ForeignKey('user_memes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent double voting
    __table_args__ = (db.UniqueConstraint('user_email', 'meme_id', name='_user_meme_uc'),)

class QuizScore(db.Model):
    __tablename__ = 'quiz_scores'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='scores')

@login_manager.user_loader
def load_user(user_email):
    return User.query.get(user_email)

# Initialize database tables
# IMPORTANT: db.create_all() only creates tables if they DON'T already exist.
# It will NOT drop or recreate existing tables, so user data is preserved.
# This is safe to run on every app startup.
with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables initialized (existing data preserved)")
    except Exception as e:
        # If table creation fails due to charset/schema issues, 
        # the app can still run. Tables should be created manually.
        error_msg = str(e).lower()
        if ('login_history' in error_msg or 'user_memes' in error_msg) and 'incompatible' in error_msg:
            print("⚠️  Some tables need manual creation (charset/schema issue)")
            print("   The app will run, but some features may be limited.")
            print("   Contact admin to fix database schema.")
        else:
            print(f"⚠️  Database initialization warning: {str(e)}")
            print("   App will continue, but some features may not work.")

# Routes
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# Auth Routes
@app.route('/login/google')
def login_google():
    print("Initiating Google Login...")
    redirect_uri = url_for('authorize_google', _external=True)
    print(f"Redirect URI: {redirect_uri}")
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize/google')
def authorize_google():
    print("Callback received from Google!")
    try:
        token = google.authorize_access_token()
        resp = google.get('userinfo')
        user_info = resp.json()
        
        print(f"Google User Info: {user_info}")
        
        # Check if user exists
        user = User.query.filter_by(email=user_info['email']).first()
        
        if not user:
            print("Creating new user...")
            user = User(
                email=user_info['email'],
                name=user_info['name'],
                picture=user_info['picture']
            )
            db.session.add(user)
            db.session.commit()
        else:
            print(f"Updating existing user: {user.email}")
            user.name = user_info['name']
            user.picture = user_info['picture']
            db.session.commit()
            
        # Use Flask-Login for session management
        login_user(user, remember=True)
        session.permanent = True
        session['user_email'] = user.email
        
        # Record login history (if table exists)
        try:
            login_record = LoginHistory(
                user_email=user.email,
                ip_address=request.headers.get('X-Forwarded-For', request.remote_addr),
                user_agent=request.headers.get('User-Agent', 'Unknown'),
                login_method='google'
            )
            db.session.add(login_record)
            db.session.commit()
            print(f"✅ User {user.email} logged in successfully! Login recorded.")
        except Exception as login_history_error:
            # If login history fails, don't block the login
            print(f"⚠️  Login successful but history not recorded: {login_history_error}")
            print(f"✅ User {user.email} logged in successfully!")
        
        return redirect('/')
        
    except Exception as e:
        error_msg = str(e).replace('\n', ' ').replace('\r', '')
        print(f"OAuth Error: {error_msg}")
        return redirect(f'/?error={error_msg}')

def get_user_from_token():
    """Fallback for API requests - check both session and current_user"""
    if current_user.is_authenticated:
        return current_user
    
    # Also check session directly
    user_email = session.get('user_email')
    if user_email:
        return User.query.get(user_email)
    
    return None

@app.route('/api/logout', methods=['POST'])
def logout():
    logout_user()
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/logout-redirect', methods=['GET', 'POST'])
def logout_redirect():
    print(f"LOGOUT: User before logout: {current_user.is_authenticated if current_user else 'No user'}")
    logout_user()
    session.clear()
    print(f"LOGOUT: Session cleared. User after logout: {current_user.is_authenticated if current_user else 'No user'}")
    
    response = redirect('/')
    
    # Prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    # Clear ALL cookies
    response.set_cookie('session', '', expires=0, path='/')
    response.set_cookie('remember_token', '', expires=0, path='/')
    
    # Add a logout flag to prevent auto-login
    response.set_cookie('just_logged_out', 'true', max_age=5, path='/')
    
    print("LOGOUT: Redirect response created with cleared cookies")
    return response


@app.route('/api/current-user', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        print(f"User authenticated: {current_user.email}")
        return jsonify({
            'authenticated': True,
            'user': {
                'email': current_user.email,
                'name': current_user.name,
                'picture': current_user.picture
            }
        })
    
    print("No user authenticated")
    return jsonify({'authenticated': False})

# Favorites Routes
@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    favorites = Favorite.query.filter_by(user_email=user.email).order_by(Favorite.saved_at.desc()).all()
    return jsonify([{
        'id': fav.id,
        'meme_id': fav.meme_id,
        'title': fav.meme_title,
        'url': fav.meme_url,
        'is_video': fav.is_video,
        'source': fav.source,
        'saved_at': fav.saved_at.isoformat()
    } for fav in favorites])

@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.json
    
    existing = Favorite.query.filter_by(
        user_email=user.email,
        meme_id=data.get('meme_id')
    ).first()
    
    if existing:
        return jsonify({'message': 'Already in favorites'}), 200
    
    favorite = Favorite(
        user_email=user.email,
        meme_id=data.get('meme_id'),
        meme_title=data.get('title'),
        meme_url=data.get('url'),
        is_video=data.get('is_video', False),
        source=data.get('source', 'Unknown')
    )
    
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Added to favorites', 'id': favorite.id}), 201

@app.route('/api/favorites/<int:fav_id>', methods=['DELETE'])
def remove_favorite(fav_id):
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    favorite = Favorite.query.filter_by(id=fav_id, user_email=user.email).first()
    
    if not favorite:
        return jsonify({'error': 'Favorite not found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Removed from favorites'})

@app.route('/api/favorites/by-meme', methods=['DELETE'])
def remove_favorite_by_meme():
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    meme_id = data.get('meme_id')
    
    if not meme_id:
        return jsonify({'error': 'meme_id required'}), 400
    
    favorite = Favorite.query.filter_by(user_email=user.email, meme_id=meme_id).first()
    
    if not favorite:
        return jsonify({'error': 'Favorite not found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Removed from favorites'})

# Quiz Categories
QUIZ_CATEGORIES = {
    'Coding & Tech': ['ProgrammerHumor', 'linuxmemes', 'programminghumor', 'softwaregore'],
    'Gaming': ['gaming', 'pcmasterrace', 'MinecraftMemes', 'LeagueOfMemes', 'GamersReactSubmission'],
    'Cute & Wholesome': ['aww', 'wholesomememes', 'Eyebleach', 'AnimalsBeingDerps', 'MadeMeSmile'],
    'Bollywood': ['bollywoodmemes', 'BollyBlindsNGossip'],
    'Desi Humor': ['IndianDankMemes', 'DesiMemes', 'bakchodi', 'IndianMeyMeys', 'HindiMemes'],
    'Global Viral': ['memes', 'dankmemes', 'me_irl', 'funny', 'facepalm', 'HolUp'],
    'Science & History': ['HistoryMemes', 'sciencememes', 'physicsmemes', 'SpaceMemes'],
    'Anime': ['animememes', 'Animemes', 'goodanimemes'],
    'Facts & Wonder': ['damnthatsinteresting', 'BeAmazed', 'interestingasfuck', 'educationalgifs'],
    'Indian Culture & Temples': ['IncredibleIndia', 'TempleArchitecture', 'Hinduism', 'IndiaSpeaks'],
    'Mythology': ['hindumemes', 'mythologymemes', 'MythologyMemes']
}

@app.route('/api/quiz/question', methods=['GET'])
def get_quiz_question():
    try:
        # 1. Pick a correct category
        correct_category = random.choice(list(QUIZ_CATEGORIES.keys()))
        
        # 2. Pick a subreddit from that category
        subreddit = random.choice(QUIZ_CATEGORIES[correct_category])
        
        # 3. Fetch meme from this subreddit
        url = f"https://meme-api.com/gimme/{subreddit}/1"
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch memes'}), 500
            
        data = response.json()
        
        # If API returns error or no memes
        if 'memes' in data and len(data['memes']) > 0:
            post = data['memes'][0]
        elif 'url' in data: # Single meme response format
            post = data
        else:
             return jsonify({'error': 'Invalid API response'}), 500

        # 4. Prepare distractors (other categories)
        all_categories = list(QUIZ_CATEGORIES.keys())
        all_categories.remove(correct_category)
        distractors = random.sample(all_categories, 3)
        
        options = distractors + [correct_category]
        random.shuffle(options)
        
        return jsonify({
            'meme_url': post.get('url'),
            'title': post.get('title'),
            'correct_answer': correct_category,
            'options': options,
            'type': 'image' if post.get('url', '').endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')) else 'video'
        })
        
    except Exception as e:
        print(f"Quiz Error: {e}")
        return jsonify({'error': str(e)}), 500

# Meme Routes
@app.route('/api/trending-memes', methods=['GET'])
def get_trending_memes():
    all_memes = []
    all_memes.extend(fetch_reddit_memes())
    all_memes.extend(fetch_imgur_memes())
    
    import random
    random.shuffle(all_memes)
    
    return jsonify(all_memes[:50])

@app.route('/api/download-proxy', methods=['GET'])
def download_proxy():
    """Proxy downloads to bypass CORS restrictions"""
    url = request.args.get('url')
    filename = request.args.get('filename', 'download')
    
    if not url:
        return jsonify({'error': 'URL required'}), 400
    
    try:
        # Fetch the file
        response = requests.get(url, stream=True, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        # Determine content type
        content_type = response.headers.get('Content-Type', 'application/octet-stream')
        
        # Create a response with the file
        return Response(
            response.iter_content(chunk_size=8192),
            content_type=content_type,
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Cache-Control': 'no-cache'
            }
        )
    except Exception as e:
        print(f"Download proxy error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/proxy-audio', methods=['GET'])
def proxy_audio():
    """Proxy Reddit audio to bypass CORS and authentication issues"""
    audio_url = request.args.get('url')
    
    if not audio_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'https://www.reddit.com/'
        }
        
        response = requests.get(audio_url, headers=headers, stream=True, timeout=10)
        
        if response.status_code == 200:
            return Response(
                response.iter_content(chunk_size=8192),
                content_type=response.headers.get('content-type', 'audio/mp4'),
                headers={
                    'Accept-Ranges': 'bytes',
                    'Content-Length': response.headers.get('content-length', '0')
                }
            )
        else:
            return jsonify({'error': f'Failed to fetch audio: {response.status_code}'}), response.status_code
            
    except Exception as e:
        print(f"Audio proxy error: {e}")
        return jsonify({'error': str(e)}), 500

def fetch_reddit_memes():
    # Use Meme API for reliable Indian content
    # We combine multiple subreddits with '+'
    # Added: Facts, Temples, Mythology, Beauty
    indian_subs = "IndianDankMemes+IndiaMemes+SaimanSays+DesiMemes+bakchodi+IndianMeyMeys+bollywoodmemes+HindiMemes+damnthatsinteresting+BeAmazed+IncredibleIndia+TempleArchitecture+hindumemes+mythologymemes+PrettyGirls"
    
    memes = []
    try:
        # Fetch 50 memes from these specific Indian subreddits
        url = f"https://meme-api.com/gimme/{indian_subs}/50"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('memes', [])
            
            # Filter for Trending: Only keep memes with > 500 upvotes
            posts = [p for p in posts if p.get('ups', 0) > 500]
            
            # Sort by upvotes (Highest first)
            posts.sort(key=lambda x: x.get('ups', 0), reverse=True)
            
            for post in posts:
                # The API already filters for images mostly, but let's be safe
                if post.get('nsfw'): 
                    continue
                    
                meme = {
                    'id': f"reddit_{post.get('postLink').split('/')[-1]}", # Extract ID from URL
                    'title': post.get('title'),
                    'ups': post.get('ups'),
                    'url': post.get('url'),
                    'is_video': False, # API usually returns images/gifs
                    'source': f"Reddit ({post.get('subreddit')})"
                }
                
                # Double check it's an image
                if meme['url'].endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                    memes.append(meme)
                    
    except Exception as e:
        print(f"Meme API error: {e}")
        
    # Fallback: If API fails, try searching Reddit for "India"
    if not memes:
        print("API failed, falling back to Reddit Search...")
        try:
            headers = {'User-Agent': 'MemeQuizApp/1.0'}
            url = 'https://www.reddit.com/search.json?q=india+meme&sort=hot&limit=50'
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', {}).get('children', [])
                process_reddit_posts(posts, memes, source='Reddit Search')
                
        except Exception as e:
            print(f"Search fallback error: {e}")

    return memes

def process_reddit_posts(posts, memes_list, source='Reddit'):
    for post in posts:
        p_data = post.get('data', {})
        
        if p_data.get('stickied') or p_data.get('is_self'):
            continue

        meme = {
            'id': f"reddit_{p_data.get('id')}",
            'title': p_data.get('title'),
            'ups': p_data.get('ups'),
            'url': p_data.get('url'),
            'is_video': p_data.get('is_video', False),
            'source': source
        }
        
        # Skip videos in this helper (videos handled separately)
        if meme['is_video'] or p_data.get('is_video'):
            continue
        
        # Skip .gifv and .mp4 links
        if meme['url'].endswith(('.mp4', '.gifv', '.gif')):
            continue

        # Validate image URLs only
        valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
        if not meme['url'].endswith(valid_extensions):
            continue

        memes_list.append(meme)

def fetch_video_memes():
    """Fetches video memes directly from Reddit JSON"""
    video_subs = ['DesiVideoMemes', 'IndianDankMemes', 'bollywoodmemes', 'IndianHumor']
    videos = []
    # Use a real browser User-Agent to avoid 429/403 errors
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for sub in video_subs:
        try:
            url = f'https://www.reddit.com/r/{sub}/hot.json?limit=25'
            response = requests.get(url, headers=headers, timeout=3)
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', {}).get('children', [])
                
                for post in posts:
                    p = post.get('data', {})
                    
                    # Check if it's a video
                    if p.get('is_video') and p.get('secure_media'):
                        video_data = p.get('secure_media', {}).get('reddit_video', {})
                        video_url = video_data.get('fallback_url')
                        
                        if video_url:
                            videos.append({
                                'id': f"reddit_vid_{p.get('id')}",
                                'title': p.get('title'),
                                'ups': p.get('ups'),
                                'url': video_url, # This is the MP4 link
                                'is_video': True,
                                'source': f"Reddit ({sub})"
                            })
        except Exception as e:
            print(f"Video fetch error {sub}: {e}")
            
    return videos

def fetch_instagram_memes():
    """Fetch real memes from Instagram using public hashtags"""
    memes = []
    try:
        # Method 1: Use Picuki (Instagram viewer) to scrape public meme pages
        # Popular meme accounts on Instagram
        meme_accounts = ['memesdaily', 'funnymemes', 'dankmemes', 'memes', 'indianmemes']
        
        import random
        selected_account = random.choice(meme_accounts)
        
        # Use a simple scraping approach for public Instagram content
        # Note: This is a simplified version. For production, consider using official APIs
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Alternative: Use meme aggregator APIs that include Instagram content
        response = requests.get(
            'https://meme-api.com/gimme/InstagramReality/20',
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'memes' in data:
                for meme in data['memes']:
                    memes.append({
                        'id': f"insta_{meme.get('postLink', '').split('/')[-1]}",
                        'title': meme.get('title', 'Instagram Meme'),
                        'url': meme.get('url'),
                        'meme_url': meme.get('url'),
                        'is_video': meme.get('url', '').endswith(('.mp4', '.gif')),
                        'source': 'Instagram',
                        'ups': meme.get('ups', random.randint(100, 500)),
                        'author': 'instagram',
                        'permalink': meme.get('postLink', '')
                    })
            print(f"✅ Fetched {len(memes)} memes from Instagram")
    except Exception as e:
        print(f"Instagram fetch error: {e}")
        # Fallback to Imgflip if Instagram fails
        try:
            response = requests.get('https://api.imgflip.com/get_memes', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    meme_templates = data.get('data', {}).get('memes', [])
                    selected = random.sample(meme_templates, min(15, len(meme_templates)))
                    
                    for meme in selected:
                        memes.append({
                            'id': f"imgflip_{meme['id']}",
                            'title': meme['name'],
                            'url': meme['url'],
                            'meme_url': meme['url'],
                            'is_video': False,
                            'source': 'Instagram',
                            'ups': random.randint(100, 500),
                            'author': 'imgflip',
                            'permalink': meme['url']
                        })
                    print(f"✅ Fetched {len(memes)} memes from Imgflip (Instagram fallback)")
        except:
            pass
    
    return memes

def fetch_tiktok_memes():
    """Fetch viral video memes from TikTok-style sources"""
    memes = []
    try:
        # Use meme APIs that aggregate TikTok-style content
        response = requests.get('https://meme-api.com/gimme/TikTokCringe/15', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'memes' in data:
                for meme in data['memes']:
                    # Only include actual videos
                    url = meme.get('url', '')
                    if url.endswith(('.mp4', '.gif', '.gifv')):
                        memes.append({
                            'id': f"tiktok_{meme.get('postLink', '').split('/')[-1]}",
                            'title': meme.get('title', 'Viral Video'),
                            'url': url,
                            'meme_url': url,
                            'is_video': True,
                            'source': 'TikTok',
                            'ups': meme.get('ups', 0),
                            'author': meme.get('author', 'tiktok'),
                            'permalink': meme.get('postLink', '')
                        })
                print(f"✅ Fetched {len(memes)} video memes from TikTok sources")
    except Exception as e:
        print(f"TikTok meme fetch error: {e}")
    
    return memes

def fetch_youtube_shorts_memes():
    """Fetch meme compilations from YouTube Shorts style content"""
    memes = []
    try:
        # Use meme APIs for video content
        response = requests.get('https://meme-api.com/gimme/videos/20', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'memes' in data:
                for meme in data['memes']:
                    url = meme.get('url', '')
                    # Filter for video content
                    if url.endswith(('.mp4', '.webm', '.gif')):
                        memes.append({
                            'id': f"yt_{meme.get('postLink', '').split('/')[-1]}",
                            'title': meme.get('title', 'Meme Video'),
                            'url': url,
                            'meme_url': url,
                            'is_video': True,
                            'source': 'YouTube',
                            'ups': meme.get('ups', 0),
                            'author': meme.get('author', 'youtube'),
                            'permalink': meme.get('postLink', '')
                        })
                print(f"✅ Fetched {len(memes)} video memes from YouTube sources")
    except Exception as e:
        print(f"YouTube meme fetch error: {e}")
    
    return memes

def fetch_twitter_memes():
    """Fetch memes from Twitter/X-style sources using meme databases"""
    memes = []
    try:
        # Use meme-api.com which aggregates from multiple sources
        response = requests.get('https://meme-api.com/gimme/memes/30', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'memes' in data:
                for meme in data['memes']:
                    # Filter for high-quality memes
                    if meme.get('ups', 0) > 100:
                        memes.append({
                            'id': f"twitter_{meme.get('postLink', '').split('/')[-1]}",
                            'title': meme.get('title', 'Trending Meme'),
                            'url': meme.get('url'),
                            'meme_url': meme.get('url'),
                            'is_video': meme.get('url', '').endswith(('.mp4', '.gif', '.gifv')),
                            'source': 'Twitter/X',
                            'ups': meme.get('ups', 0),
                            'author': meme.get('author', 'twitter'),
                            'permalink': meme.get('postLink', '')
                        })
                print(f"✅ Fetched {len(memes)} memes from Twitter/X sources")
    except Exception as e:
        print(f"Twitter meme fetch error: {e}")
    
    return memes

def fetch_9gag_memes():
    """Fetch trending memes from 9GAG-style sources"""
    memes = []
    try:
        # Use another meme API endpoint
        response = requests.get('https://meme-api.com/gimme/dankmemes/25', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'memes' in data:
                for meme in data['memes']:
                    memes.append({
                        'id': f"9gag_{meme.get('postLink', '').split('/')[-1]}",
                        'title': meme.get('title', 'Dank Meme'),
                        'url': meme.get('url'),
                        'meme_url': meme.get('url'),
                        'is_video': meme.get('url', '').endswith(('.mp4', '.gif', '.gifv')),
                        'source': '9GAG',
                        'ups': meme.get('ups', 0),
                        'author': meme.get('author', '9gag'),
                        'permalink': meme.get('postLink', '')
                    })
                print(f"✅ Fetched {len(memes)} memes from 9GAG sources")
    except Exception as e:
        print(f"9GAG meme fetch error: {e}")
    
    return memes

@app.route('/api/memes')
def get_memes():
    """Fetch memes from multiple sources for diversity"""
    all_memes = []
    
    # Fetch from multiple sources in parallel for speed
    import concurrent.futures
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        futures = {
            executor.submit(fetch_reddit_memes): 'Reddit',
            executor.submit(fetch_instagram_memes): 'Instagram',
            executor.submit(fetch_twitter_memes): 'Twitter',
            executor.submit(fetch_9gag_memes): '9GAG',
            executor.submit(fetch_tiktok_memes): 'TikTok',
            executor.submit(fetch_youtube_shorts_memes): 'YouTube',
        }
        
        for future in concurrent.futures.as_completed(futures):
            source = futures[future]
            try:
                memes = future.result()
                all_memes.extend(memes)
                print(f"✅ {source}: {len(memes)} memes")
            except Exception as e:
                print(f"❌ {source} failed: {e}")
    
    # Shuffle for variety
    import random
    random.shuffle(all_memes)
    
    # Limit to 120 memes to avoid overwhelming the client
    all_memes = all_memes[:120]
    
    print(f"🎯 Total memes returned: {len(all_memes)}")
    return jsonify(all_memes)

def fetch_imgur_memes():
    memes = []
    try:
        url = 'https://meme-api.com/gimme/30'
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('memes', [])
            
            for item in items:
                url = item.get('url', '')
                import hashlib
                unique_id = hashlib.md5(url.encode()).hexdigest()[:12] if url else 'unknown'
                
                meme = {
                    'id': f"memeapi_{unique_id}",
                    'title': item.get('title', 'Viral Meme')[:100],
                    'ups': item.get('ups', 0),
                    'is_video': url.endswith(('.mp4', '.gif')),
                    'url': url,
                    'source': 'Meme API'
                }
                
                # TEMPORARILY SKIP VIDEOS - only show images
                if meme['is_video'] or url.endswith(('.mp4', '.gif', '.gifv')):
                    continue
                
                if meme['url']:
                    memes.append(meme)
                        
    except Exception as e:
        print(f"Meme API fetch error: {e}")
    
    return memes

@app.route('/api/post-meme', methods=['POST'])
@login_required
def post_meme():
    try:
        # Check if UserMeme table exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if 'user_memes' not in inspector.get_table_names():
            return jsonify({'error': 'Feature not available yet. Please contact admin.'}), 503
        
        data = request.get_json()
        image_data = data.get('image_data')
        title = data.get('title', 'Untitled Meme')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Create new meme
        new_meme = UserMeme(
            user_email=current_user.email,
            title=title,
            image_data=image_data
        )
        
        db.session.add(new_meme)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'meme_id': new_meme.id,
            'message': 'Meme posted successfully!'
        })
    except Exception as e:
        print(f"Error posting meme: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to post meme. Feature may not be available yet.'}), 500

@app.route('/api/user-memes', methods=['GET'])
def get_user_memes():
    try:
        # Check if UserMeme table exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if 'user_memes' not in inspector.get_table_names():
            return jsonify([])  # Return empty array if table doesn't exist
        
        user = get_user_from_token()
        
        # Get recent user-generated memes
        memes = UserMeme.query.order_by(UserMeme.created_at.desc()).limit(50).all()
        
        result = []
        for meme in memes:
            has_upvoted = False
            if user:
                has_upvoted = Upvote.query.filter_by(user_email=user.email, meme_id=meme.id).first() is not None

            result.append({
                'id': meme.id, # Integer ID for internal use
                'display_id': f'user_{meme.id}', # String ID for frontend
                'title': meme.title,
                'url': meme.image_data,  # Base64 data URL
                'author': meme.user.name if meme.user else 'Anonymous',
                'author_pic': meme.user.picture if meme.user else None,
                'ups': meme.upvotes,
                'has_upvoted': has_upvoted,
                'comment_count': Comment.query.filter_by(meme_id=meme.id).count(),
                'source': 'user_generated',
                'isVideo': False,
                'created_at': meme.created_at.isoformat()
            })
        
        return jsonify(result)
    except Exception as e:
        print(f"Error fetching user memes: {str(e)}")
        return jsonify([])  # Return empty array on error

@app.route('/api/memes/<int:meme_id>/upvote', methods=['POST'])
def upvote_meme(meme_id):
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    meme = UserMeme.query.get(meme_id)
    if not meme:
        return jsonify({'error': 'Meme not found'}), 404
        
    existing_vote = Upvote.query.filter_by(user_email=user.email, meme_id=meme_id).first()
    
    if existing_vote:
        # Toggle off
        db.session.delete(existing_vote)
        meme.upvotes = max(0, meme.upvotes - 1)
        action = 'removed'
    else:
        # Toggle on
        vote = Upvote(user_email=user.email, meme_id=meme_id)
        db.session.add(vote)
        meme.upvotes += 1
        action = 'added'
        
    db.session.commit()
    return jsonify({'success': True, 'upvotes': meme.upvotes, 'action': action})

@app.route('/api/memes/<int:meme_id>/comments', methods=['GET', 'POST'])
def handle_comments(meme_id):
    if request.method == 'POST':
        user = get_user_from_token()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
            
        data = request.json
        content = data.get('content')
        if not content:
            return jsonify({'error': 'Content required'}), 400
            
        comment = Comment(user_email=user.email, meme_id=meme_id, content=content)
        db.session.add(comment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'comment': {
                'id': comment.id,
                'user': user.name,
                'picture': user.picture,
                'content': comment.content,
                'created_at': comment.created_at.isoformat()
            }
        })
    else:
        comments = Comment.query.filter_by(meme_id=meme_id).order_by(Comment.created_at.desc()).all()
        return jsonify([{
            'id': c.id,
            'user': c.user.name,
            'picture': c.user.picture,
            'content': c.content,
            'created_at': c.created_at.isoformat()
        } for c in comments])

@app.route('/api/quiz/score', methods=['POST'])
def save_quiz_score():
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.json
    score = data.get('score', 0)
    
    new_score = QuizScore(user_email=user.email, score=score)
    db.session.add(new_score)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        # Top Quiz Scores
        top_scores = db.session.query(
            User.name, User.picture, db.func.max(QuizScore.score).label('max_score')
        ).join(QuizScore).group_by(User.email).order_by(db.desc('max_score')).limit(10).all()
        
        # Top Meme Creators (by total upvotes)
        top_creators = db.session.query(
            User.name, User.picture, db.func.sum(UserMeme.upvotes).label('total_upvotes')
        ).join(UserMeme).group_by(User.email).order_by(db.desc('total_upvotes')).limit(10).all()
        
        return jsonify({
            'quiz_leaders': [{'name': r[0], 'picture': r[1], 'score': r[2]} for r in top_scores],
            'meme_leaders': [{'name': r[0], 'picture': r[1], 'upvotes': int(r[2] or 0)} for r in top_creators]
        })
    except Exception as e:
        print(f"Leaderboard error: {e}")
        return jsonify({'quiz_leaders': [], 'meme_leaders': []})

if __name__ == '__main__':
    print("Starting MemeMaster Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
