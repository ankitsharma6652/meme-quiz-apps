"""
Migration script to add LoginHistory table to existing database.
Run this on PythonAnywhere to add the new table without affecting existing data.
"""

import os
import sys
from datetime import datetime

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, LoginHistory

def add_login_history_table():
    """Add LoginHistory table to the database"""
    with app.app_context():
        try:
            # Check if table already exists
            inspector = db.inspect(db.engine)
            if 'login_history' in inspector.get_table_names():
                print("✅ LoginHistory table already exists!")
                return
            
            # Create only the LoginHistory table
            LoginHistory.__table__.create(db.engine)
            print("✅ LoginHistory table created successfully!")
            
        except Exception as e:
            print(f"❌ Error creating LoginHistory table: {e}")
            raise

if __name__ == '__main__':
    print("Adding LoginHistory table to database...")
    add_login_history_table()
    print("Migration complete!")
