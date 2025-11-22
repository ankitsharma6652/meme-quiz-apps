"""
Migration script to add UserMeme table to the database
Run this on PythonAnywhere console or locally
"""

from app import app, db, UserMeme
import sys

def migrate():
    with app.app_context():
        try:
            print("Creating UserMeme table...")
            db.create_all()
            print("✅ UserMeme table created successfully!")
            print("\nYou can now use the Post Meme feature.")
            return True
        except Exception as e:
            print(f"❌ Error creating table: {str(e)}")
            return False

if __name__ == '__main__':
    print("=" * 50)
    print("UserMeme Table Migration")
    print("=" * 50)
    
    success = migrate()
    
    if success:
        print("\n✅ Migration completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)
