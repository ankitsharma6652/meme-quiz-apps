"""
Safe migration to add LoginHistory table with proper charset/collation matching.
This script creates the table using raw SQL to ensure compatibility.
"""

import os
import sys
from datetime import datetime

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def add_login_history_table_safe():
    """Add LoginHistory table using raw SQL to ensure charset compatibility"""
    with app.app_context():
        try:
            # Check if table already exists
            result = db.session.execute(db.text("SHOW TABLES LIKE 'login_history'"))
            if result.fetchone():
                print("✅ LoginHistory table already exists!")
                return
            
            # Get the charset and collation from the user table
            result = db.session.execute(db.text("""
                SELECT CCSA.character_set_name, CCSA.collation_name
                FROM information_schema.`COLUMNS` C
                JOIN information_schema.`COLLATION_CHARACTER_SET_APPLICABILITY` CCSA
                ON (C.collation_name = CCSA.collation_name)
                WHERE C.table_schema = DATABASE()
                AND C.table_name = 'user'
                AND C.column_name = 'email'
            """))
            charset_info = result.fetchone()
            
            if charset_info:
                charset = charset_info[0]
                collation = charset_info[1]
                print(f"Using charset: {charset}, collation: {collation}")
            else:
                # Default to utf8mb4 if we can't determine
                charset = 'utf8mb4'
                collation = 'utf8mb4_unicode_ci'
                print(f"Using default charset: {charset}, collation: {collation}")
            
            # Create the table with matching charset/collation
            create_table_sql = f"""
            CREATE TABLE login_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_email VARCHAR(120) CHARACTER SET {charset} COLLATE {collation} NOT NULL,
                login_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                ip_address VARCHAR(45),
                user_agent VARCHAR(500),
                login_method VARCHAR(50) DEFAULT 'google',
                INDEX idx_user_email (user_email),
                INDEX idx_login_time (login_time),
                FOREIGN KEY (user_email) REFERENCES user(email) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET={charset} COLLATE={collation};
            """
            
            db.session.execute(db.text(create_table_sql))
            db.session.commit()
            print("✅ LoginHistory table created successfully with proper charset/collation!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating LoginHistory table: {e}")
            raise

if __name__ == '__main__':
    print("Adding LoginHistory table to database (safe mode)...")
    add_login_history_table_safe()
    print("Migration complete!")
