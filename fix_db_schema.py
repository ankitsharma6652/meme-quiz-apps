import os
import pymysql
from urllib.parse import quote_plus

print("="*60)
print("🔧 DATABASE SCHEMA FIX")
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
    
    # 1. Add 'is_video' column
    print("\n1. Checking 'is_video' column...")
    try:
        cursor.execute("SELECT is_video FROM favorite LIMIT 1")
        print("   ✅ Column 'is_video' already exists.")
    except:
        print("   ⚠️  Column 'is_video' missing. Adding it...")
        cursor.execute("ALTER TABLE favorite ADD COLUMN is_video BOOLEAN DEFAULT FALSE")
        print("   ✅ Added 'is_video' column.")

    # 2. Add 'source' column
    print("\n2. Checking 'source' column...")
    try:
        cursor.execute("SELECT source FROM favorite LIMIT 1")
        print("   ✅ Column 'source' already exists.")
    except:
        print("   ⚠️  Column 'source' missing. Adding it...")
        cursor.execute("ALTER TABLE favorite ADD COLUMN source VARCHAR(50) DEFAULT 'Unknown'")
        print("   ✅ Added 'source' column.")

    # 3. Fix 'created_at' -> 'saved_at'
    print("\n3. Checking 'saved_at' column...")
    try:
        cursor.execute("SELECT saved_at FROM favorite LIMIT 1")
        print("   ✅ Column 'saved_at' already exists.")
    except:
        print("   ⚠️  Column 'saved_at' missing. Checking for 'created_at'...")
        try:
            cursor.execute("SELECT created_at FROM favorite LIMIT 1")
            print("   ⚠️  Renaming 'created_at' to 'saved_at'...")
            cursor.execute("ALTER TABLE favorite CHANGE COLUMN created_at saved_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            print("   ✅ Renamed successfully.")
        except:
            print("   ⚠️  Neither exists. Adding 'saved_at'...")
            cursor.execute("ALTER TABLE favorite ADD COLUMN saved_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            print("   ✅ Added 'saved_at' column.")

    conn.commit()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ DATABASE SCHEMA FIXED SUCCESSFULLY!")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
