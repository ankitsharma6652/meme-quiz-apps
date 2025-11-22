#!/usr/bin/env python3
"""
Database Migration Script: SQLite to MySQL
Migrates data from local SQLite to PythonAnywhere MySQL
"""

import sqlite3
import pymysql
import os
from datetime import datetime

# MySQL Configuration (update these with your actual values)
MYSQL_CONFIG = {
    'host': 'ankitsharma6652.mysql.pythonanywhere-services.com',
    'user': 'ankitsharma6652',
    'password': os.environ.get('MYSQL_PASSWORD', ''),  # Set this in environment
    'database': 'ankitsharma6652$mememaster',
    'charset': 'utf8mb4'
}

def create_mysql_tables(mysql_conn):
    """Create tables in MySQL if they don't exist"""
    cursor = mysql_conn.cursor()
    
    # Create user table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            name VARCHAR(255),
            picture TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_email (email)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    
    # Create favorite table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            meme_id VARCHAR(255) NOT NULL,
            meme_url TEXT,
            meme_title TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
            UNIQUE KEY unique_user_meme (user_id, meme_id),
            INDEX idx_user_id (user_id),
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    
    mysql_conn.commit()
    print("✅ MySQL tables created successfully")

def migrate_users(sqlite_conn, mysql_conn):
    """Migrate users from SQLite to MySQL"""
    sqlite_cursor = sqlite_conn.cursor()
    mysql_cursor = mysql_conn.cursor()
    
    # Get all users from SQLite
    sqlite_cursor.execute("SELECT id, email, name, picture, created_at FROM user")
    users = sqlite_cursor.fetchall()
    
    migrated = 0
    skipped = 0
    
    for user in users:
        user_id, email, name, picture, created_at = user
        try:
            # Insert or update user in MySQL
            mysql_cursor.execute("""
                INSERT INTO user (email, name, picture, created_at)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    picture = VALUES(picture)
            """, (email, name, picture, created_at))
            migrated += 1
        except Exception as e:
            print(f"⚠️  Error migrating user {email}: {e}")
            skipped += 1
    
    mysql_conn.commit()
    print(f"✅ Migrated {migrated} users ({skipped} skipped)")
    return migrated

def migrate_favorites(sqlite_conn, mysql_conn):
    """Migrate favorites from SQLite to MySQL"""
    sqlite_cursor = sqlite_conn.cursor()
    mysql_cursor = mysql_conn.cursor()
    
    # Get all favorites from SQLite with user email
    sqlite_cursor.execute("""
        SELECT f.id, u.email, f.meme_id, f.meme_url, f.meme_title, f.created_at
        FROM favorite f
        JOIN user u ON f.user_id = u.id
    """)
    favorites = sqlite_cursor.fetchall()
    
    migrated = 0
    skipped = 0
    
    for fav in favorites:
        fav_id, email, meme_id, meme_url, meme_title, created_at = fav
        try:
            # Get MySQL user_id from email
            mysql_cursor.execute("SELECT id FROM user WHERE email = %s", (email,))
            result = mysql_cursor.fetchone()
            
            if result:
                mysql_user_id = result[0]
                
                # Insert or ignore favorite in MySQL
                mysql_cursor.execute("""
                    INSERT IGNORE INTO favorite (user_id, meme_id, meme_url, meme_title, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (mysql_user_id, meme_id, meme_url, meme_title, created_at))
                migrated += 1
            else:
                print(f"⚠️  User not found for favorite: {email}")
                skipped += 1
        except Exception as e:
            print(f"⚠️  Error migrating favorite {meme_id}: {e}")
            skipped += 1
    
    mysql_conn.commit()
    print(f"✅ Migrated {migrated} favorites ({skipped} skipped)")
    return migrated

def main():
    print("=" * 80)
    print("DATABASE MIGRATION: SQLite → MySQL")
    print("=" * 80)
    
    # Check if SQLite database exists
    if not os.path.exists('mememaster.db'):
        print("❌ SQLite database 'mememaster.db' not found!")
        print("   Make sure you're running this from the project directory.")
        return
    
    # Check MySQL password
    if not MYSQL_CONFIG['password']:
        print("❌ MySQL password not set!")
        print("   Set MYSQL_PASSWORD environment variable:")
        print("   export MYSQL_PASSWORD='your-mysql-password'")
        return
    
    try:
        # Connect to SQLite
        print("\n📂 Connecting to SQLite database...")
        sqlite_conn = sqlite3.connect('mememaster.db')
        print("✅ Connected to SQLite")
        
        # Connect to MySQL
        print("\n🔌 Connecting to MySQL database...")
        mysql_conn = pymysql.connect(**MYSQL_CONFIG)
        print("✅ Connected to MySQL")
        
        # Create tables
        print("\n📋 Creating MySQL tables...")
        create_mysql_tables(mysql_conn)
        
        # Migrate users
        print("\n👥 Migrating users...")
        users_migrated = migrate_users(sqlite_conn, mysql_conn)
        
        # Migrate favorites
        print("\n❤️  Migrating favorites...")
        favorites_migrated = migrate_favorites(sqlite_conn, mysql_conn)
        
        # Summary
        print("\n" + "=" * 80)
        print("MIGRATION COMPLETE!")
        print("=" * 80)
        print(f"✅ Users migrated: {users_migrated}")
        print(f"✅ Favorites migrated: {favorites_migrated}")
        print("\nNext steps:")
        print("1. Update .env file on PythonAnywhere with MySQL credentials")
        print("2. Set PYTHONANYWHERE_DOMAIN environment variable")
        print("3. Reload your web app")
        print("=" * 80)
        
    except pymysql.Error as e:
        print(f"\n❌ MySQL Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your MySQL password")
        print("2. Verify database name: ankitsharma6652$mememaster")
        print("3. Ensure MySQL database is created on PythonAnywhere")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'sqlite_conn' in locals():
            sqlite_conn.close()
        if 'mysql_conn' in locals():
            mysql_conn.close()

if __name__ == "__main__":
    main()
