import os
import pymysql
from urllib.parse import quote_plus

print("="*60)
print("🧨 DATABASE RESET (DROP & RECREATE)")
print("="*60)

# Configuration
MYSQL_HOST = 'ankitsharma6652.mysql.pythonanywhere-services.com'
MYSQL_USER = 'ankitsharma6652'
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DB = 'ankitsharma6652$mememaster'

if not MYSQL_PASSWORD:
    print("❌ Error: MYSQL_PASSWORD environment variable is not set.")
    print("   Run: export MYSQL_PASSWORD='your-password'")
    exit(1)

try:
    print(f"🔌 Connecting to {MYSQL_DB}...")
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    print("✅ Connected successfully!")
    
    cursor = conn.cursor()
    
    # 1. Drop Tables
    print("\n1. Dropping existing tables...")
    try:
        cursor.execute("DROP TABLE IF EXISTS favorite")
        print("   🗑️  Dropped 'favorite'")
        cursor.execute("DROP TABLE IF EXISTS user")
        print("   🗑️  Dropped 'user'")
    except Exception as e:
        print(f"   ⚠️  Error dropping tables: {e}")

    # 2. Create User Table
    print("\n2. Creating 'user' table (PK: email)...")
    cursor.execute("""
        CREATE TABLE user (
            email VARCHAR(120) PRIMARY KEY,
            name VARCHAR(120),
            picture VARCHAR(500),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("   ✅ Done")
    
    # 3. Create Favorite Table
    print("\n3. Creating 'favorite' table (FK: user_email)...")
    cursor.execute("""
        CREATE TABLE favorite (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_email VARCHAR(120) NOT NULL,
            meme_id VARCHAR(200) NOT NULL,
            meme_title VARCHAR(500),
            meme_url VARCHAR(1000),
            is_video BOOLEAN DEFAULT FALSE,
            source VARCHAR(50) DEFAULT 'Unknown',
            saved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES user(email) ON DELETE CASCADE,
            UNIQUE KEY unique_user_meme (user_email, meme_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("   ✅ Done")
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ DATABASE RESET COMPLETE!")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
