from flask import Flask, request, jsonify, send_from_directory, Response, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import requests
import os
import html
import secrets
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Allow OAuth over HTTP for localhost
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='', static_folder='.')

# Configuration
# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mememaster.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session Configuration (Fix for Localhost)
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
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120))
    picture = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    favorites = db.relationship('Favorite', backref='user', lazy=True, cascade='all, delete-orphan')

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meme_id = db.Column(db.String(200), nullable=False)
    meme_title = db.Column(db.String(500))
    meme_url = db.Column(db.String(1000))
    is_video = db.Column(db.Boolean, default=False)
    source = db.Column(db.String(50))
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()
    print("Database tables created!")

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
        session['user_id'] = user.id
        
        print(f"User {user.email} logged in successfully!")
        
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
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    
    return None

@app.route('/api/logout', methods=['POST'])
def logout():
    logout_user()
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/logout-redirect', methods=['GET', 'POST'])
def logout_redirect():
    logout_user()
    session.clear()
    response = redirect('/')
    # Prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/api/current-user', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        print(f"User authenticated: {current_user.email}")
        return jsonify({
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'name': current_user.name,
                'email': current_user.email,
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
        
    favorites = Favorite.query.filter_by(user_id=user.id).order_by(Favorite.saved_at.desc()).all()
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
        user_id=user.id,
        meme_id=data.get('meme_id')
    ).first()
    
    if existing:
        return jsonify({'message': 'Already in favorites'}), 200
    
    favorite = Favorite(
        user_id=user.id,
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
        
    favorite = Favorite.query.filter_by(id=fav_id, user_id=user.id).first()
    
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
    
    favorite = Favorite.query.filter_by(user_id=user.id, meme_id=meme_id).first()
    
    if not favorite:
        return jsonify({'error': 'Favorite not found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Removed from favorites'})

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
    # Prioritize Indian subreddits
    subreddits = ['IndiaMemes', 'IndianDankMemes', 'bakchodi', 'IndianMeyMeys', 'memes', 'dankmemes']
    memes = []
    headers = {'User-Agent': 'MemeQuizApp/1.0'}
    
    try:
        # Fetch more from Indian subreddits (first 4 are Indian)
        for i, sub in enumerate(subreddits[:6]):
            # Get more posts from Indian subreddits
            limit = 30 if i < 4 else 15
            url = f'https://www.reddit.com/r/{sub}/hot.json?limit={limit}'
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code != 200:
                continue
                
            data = response.json()
            posts = data.get('data', {}).get('children', [])

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
                    'source': 'Reddit'
                }
                
                # TEMPORARILY SKIP ALL VIDEOS - only show images
                if meme['is_video'] or p_data.get('is_video'):
                    continue
                
                # Handle Reddit videos (DISABLED FOR NOW)
                # if meme['is_video'] and p_data.get('secure_media'):
                #     video_data = p_data.get('secure_media', {}).get('reddit_video', {})
                #     fallback_url = video_data.get('fallback_url')  # Most reliable
                #     
                #     if fallback_url:
                #         meme['video_url'] = html.unescape(fallback_url)
                #         meme['url'] = meme['video_url']
                #     else:
                #         meme['is_video'] = False
                
                # Skip .gifv and .mp4 links
                if meme['url'].endswith(('.mp4', '.gifv', '.gif')):
                    continue

                # Validate image URLs only
                valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
                if not meme['url'].endswith(valid_extensions):
                    continue

                memes.append(meme)
    except Exception as e:
        print(f"Reddit fetch error: {e}")
    
    return memes

def fetch_imgur_memes():
    memes = []
    try:
        url = 'https://meme-api.com/gimme/30'
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('memes', [])
            
            for item in items:
                # Generate unique ID from URL
                import hashlib
                url = item.get('url', '')
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

if __name__ == '__main__':
    print("Starting MemeMaster Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
