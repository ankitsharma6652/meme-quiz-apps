#!/usr/bin/env python3
"""
Database Viewer for MemeMaster
Works for both local and PythonAnywhere databases
"""

import sqlite3
import os
from datetime import datetime

def view_database(db_path='mememaster.db'):
    if not os.path.exists(db_path):
        print(f"❌ Database file '{db_path}' not found!")
        print("\nTo view PythonAnywhere database:")
        print("1. SSH into PythonAnywhere")
        print("2. cd meme-quiz-apps")
        print("3. python3 view_database.py")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 80)
    print("MEMEMASTER DATABASE VIEWER")
    print("=" * 80)
    print(f"Database: {db_path}")
    print(f"Size: {os.path.getsize(db_path) / 1024:.2f} KB")
    
    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"\nTables: {', '.join([t[0] for t in tables])}")
    
    # View Users
    print("\n📊 USERS TABLE:")
    print("-" * 80)
    try:
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        
        if users:
            print(f"{'ID':<5} {'Email':<35} {'Name':<25} {'Created':<20}")
            print("-" * 80)
            for user in users:
                user_id, email, name, picture, created = user
                created_date = datetime.fromisoformat(created).strftime('%Y-%m-%d %H:%M')
                print(f"{user_id:<5} {email:<35} {name:<25} {created_date:<20}")
            print(f"\n✅ Total Users: {len(users)}")
        else:
            print("No users found.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    
    # View Favorites
    print("\n\n❤️  FAVORITES TABLE:")
    print("-" * 80)
    try:
        cursor.execute("""
            SELECT f.id, u.email, f.meme_id, f.meme_title, f.created_at 
            FROM favorite f 
            JOIN user u ON f.user_id = u.id 
            ORDER BY f.created_at DESC
            LIMIT 20
        """)
        favorites = cursor.fetchall()
        
        if favorites:
            print(f"{'ID':<5} {'User Email':<35} {'Meme ID':<25} {'Created':<20}")
            print("-" * 80)
            for fav in favorites:
                fav_id, email, meme_id, meme_title, created = fav
                created_date = datetime.fromisoformat(created).strftime('%Y-%m-%d %H:%M')
                meme_id_short = meme_id[:22] + '...' if len(meme_id) > 25 else meme_id
                print(f"{fav_id:<5} {email:<35} {meme_id_short:<25} {created_date:<20}")
            
            cursor.execute("SELECT COUNT(*) FROM favorite")
            total = cursor.fetchone()[0]
            print(f"\n✅ Total Favorites: {total} (showing latest 20)")
        else:
            print("No favorites found.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    
    # Statistics
    print("\n\n📈 STATISTICS:")
    print("-" * 80)
    
    try:
        cursor.execute("SELECT COUNT(*) FROM user")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM favorite")
        favorite_count = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT u.email, u.name, COUNT(f.id) as fav_count 
            FROM user u 
            LEFT JOIN favorite f ON u.id = f.user_id 
            GROUP BY u.id 
            ORDER BY fav_count DESC 
            LIMIT 10
        """)
        top_users = cursor.fetchall()
        
        print(f"📊 Total Users: {user_count}")
        print(f"❤️  Total Favorites: {favorite_count}")
        if user_count > 0:
            print(f"📈 Average Favorites per User: {favorite_count / user_count:.2f}")
        
        if top_users:
            print("\n🏆 Top Users by Favorites:")
            for email, name, count in top_users:
                print(f"  {count:>3} favorites - {name} ({email})")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    
    conn.close()
    print("\n" + "=" * 80)

if __name__ == "__main__":
    import sys
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'mememaster.db'
    
    try:
        view_database(db_path)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
