import os
import pymysql
import sys

print("="*60)
print("🕵️‍♂️ DEPLOYMENT VERIFICATION")
print("="*60)

# 1. Check Code (app.py)
print("\n1. Checking Code (app.py)...")
try:
    with open('app.py', 'r') as f:
        content = f.read()
        if 'user_email = db.Column' in content:
            print("   ✅ Code is UPDATED (Uses 'user_email')")
        else:
            print("   ❌ Code is OUTDATED (Still uses 'user_id'?)")
            print("   👉 ACTION: You need to run 'git pull'")
except Exception as e:
    print(f"   ⚠️ Error reading app.py: {e}")

# 2. Check Database Schema
print("\n2. Checking Database Schema...")
MYSQL_HOST = 'ankitsharma6652.mysql.pythonanywhere-services.com'
MYSQL_USER = 'ankitsharma6652'
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DB = 'ankitsharma6652$mememaster'

if not MYSQL_PASSWORD:
    print("   ❌ MYSQL_PASSWORD not set. Cannot check DB.")
else:
    try:
        conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)
        cursor = conn.cursor()
        cursor.execute("DESCRIBE favorite")
        columns = [row[0] for row in cursor.fetchall()]
        
        if 'user_email' in columns:
            print("   ✅ Database is UPDATED (Has 'user_email' column)")
        elif 'user_id' in columns:
            print("   ❌ Database is OUTDATED (Has 'user_id' column)")
            print("   👉 ACTION: You need to run 'python3.10 reset_db.py'")
        else:
            print(f"   ⚠️ Unknown Schema: {columns}")
            
        conn.close()
    except Exception as e:
        print(f"   ❌ DB Connection Error: {e}")

print("\n" + "="*60)
