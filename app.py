from flask import Flask, request, jsonify, send_from_directory, Response, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import requests
import os
import html
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_url_path='', static_folder='.')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mememaster.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    redirect_uri = url_for('authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize/google')
def authorize_google():
    try:
        token = google.authorize_access_token()
        resp = google.get('userinfo')
        user_info = resp.json()
        
        # Check if user exists
        user = User.query.filter_by(email=user_info['email']).first()
        
        if not user:
            # Create new user
            user = User(
                email=user_info['email'],
                name=user_info['name'],
                picture=user_info['picture']
            )
            db.session.add(user)
            db.session.commit()
        else:
            # Update existing user info
            user.name = user_info['name']
            user.picture = user_info['picture']
            db.session.commit()
            
        login_user(user)
        return redirect('/')
        
    except Exception as e:
        print(f"OAuth Error: {e}")
        return redirect('/')

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/current-user', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'name': current_user.name,
                'email': current_user.email,
                'picture': current_user.picture
            }
        })
    return jsonify({'authenticated': False})

# Favorites Routes
@app.route('/api/favorites', methods=['GET'])
@login_required
def get_favorites():
    favorites = Favorite.query.filter_by(user_id=current_user.id).order_by(Favorite.saved_at.desc()).all()
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
@login_required
def add_favorite():
    data = request.json
    
    existing = Favorite.query.filter_by(
        user_id=current_user.id,
        meme_id=data.get('meme_id')
    ).first()
    
    if existing:
        return jsonify({'message': 'Already in favorites'}), 200
    
    favorite = Favorite(
        user_id=current_user.id,
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
@login_required
def remove_favorite(fav_id):
    favorite = Favorite.query.filter_by(id=fav_id, user_id=current_user.id).first()
    
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
    subreddits = ['IndiaMemes', 'IndianDankMemes', 'bakchodi', 'memes', 'dankmemes', 'funny']
    memes = []
    headers = {'User-Agent': 'MemeQuizApp/1.0'}
    
    try:
        for sub in subreddits[:4]:
            url = f'https://www.reddit.com/r/{sub}/hot.json?limit=20'
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

                if meme['is_video'] and p_data.get('secure_media'):
                    video_data = p_data.get('secure_media', {}).get('reddit_video', {})
                    fallback_url = video_data.get('fallback_url')
                    if fallback_url:
                        meme['video_url'] = html.unescape(fallback_url)
                        meme['url'] = meme['video_url']
                    else:
                        meme['is_video'] = False
                
                if not meme['is_video'] and meme['url'].endswith(('.mp4', '.gifv')):
                     meme['is_video'] = True
                     meme['video_url'] = meme['url'].replace('.gifv', '.mp4')

                if meme['is_video'] and not meme.get('video_url'):
                    continue

                valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4')
                if not meme['is_video'] and not meme['url'].endswith(valid_extensions):
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
                meme = {
                    'id': f"memeapi_{item.get('postLink', '').split('/')[-2]}",
                    'title': item.get('title', 'Viral Meme')[:100],
                    'ups': item.get('ups', 0),
                    'is_video': item.get('url', '').endswith(('.mp4', '.gif')),
                    'url': item.get('url', ''),
                    'source': 'Imgur'
                }
                
                if meme['is_video']:
                    meme['video_url'] = meme['url']
                
                if meme['url']:
                    memes.append(meme)
                        
    except Exception as e:
        print(f"Meme API fetch error: {e}")
    
    return memes

if __name__ == '__main__':
    print("Starting MemeMaster Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
