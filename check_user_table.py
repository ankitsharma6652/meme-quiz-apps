"""
Check the actual structure of the user table to diagnose the foreign key issue.
Run this on PythonAnywhere to see the exact column definition.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def check_user_table_structure():
    """Check the actual structure of the user table"""
    with app.app_context():
        try:
            # Get the full column definition for user.email
            result = db.session.execute(db.text("""
                SHOW CREATE TABLE user
            """))
            create_statement = result.fetchone()
            print("=" * 80)
            print("USER TABLE STRUCTURE:")
            print("=" * 80)
            print(create_statement[1])
            print("=" * 80)
            
            # Get specific column info
            result = db.session.execute(db.text("""
                SELECT 
                    COLUMN_NAME,
                    COLUMN_TYPE,
                    CHARACTER_SET_NAME,
                    COLLATION_NAME,
                    COLUMN_KEY,
                    EXTRA
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'user'
                AND COLUMN_NAME = 'email'
            """))
            
            column_info = result.fetchone()
            if column_info:
                print("\nEMAIL COLUMN DETAILS:")
                print(f"  Column Name: {column_info[0]}")
                print(f"  Column Type: {column_info[1]}")
                print(f"  Character Set: {column_info[2]}")
                print(f"  Collation: {column_info[3]}")
                print(f"  Key: {column_info[4]}")
                print(f"  Extra: {column_info[5]}")
            
            # Check if login_history table exists
            result = db.session.execute(db.text("SHOW TABLES LIKE 'login_history'"))
            if result.fetchone():
                print("\n⚠️  login_history table already exists!")
                result = db.session.execute(db.text("SHOW CREATE TABLE login_history"))
                create_statement = result.fetchone()
                print("\nLOGIN_HISTORY TABLE STRUCTURE:")
                print("=" * 80)
                print(create_statement[1])
                print("=" * 80)
            else:
                print("\n✅ login_history table does not exist yet")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            raise

if __name__ == '__main__':
    check_user_table_structure()
