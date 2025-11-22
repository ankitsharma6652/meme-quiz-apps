import os
import pymysql

print("="*60)
print("🛠️  DATABASE INITIALIZATION")
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
    
    # Create User Table
    print("\n1. Creating 'user' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            name VARCHAR(255),
            picture TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("   ✅ Done")
    
    # Create Favorite Table
    print("\n2. Creating 'favorite' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            meme_id VARCHAR(255) NOT NULL,
            meme_url TEXT,
            meme_title TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
            UNIQUE KEY unique_user_meme (user_id, meme_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("   ✅ Done")
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ DATABASE INITIALIZED SUCCESSFULLY!")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
