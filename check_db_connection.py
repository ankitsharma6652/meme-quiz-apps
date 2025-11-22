import os
import sys
import pymysql

print("="*60)
print("🔍 DIAGNOSTIC: Database Connection Check")
print("="*60)

# 1. Check Environment Variables
print("\n1. Checking Environment Variables:")
mysql_password = os.environ.get('MYSQL_PASSWORD')
if mysql_password:
    print(f"   ✅ MYSQL_PASSWORD is set (length: {len(mysql_password)})")
else:
    print("   ❌ MYSQL_PASSWORD is NOT set!")
    print("      Run: export MYSQL_PASSWORD='your-password'")

# 2. Check PyMySQL Installation
print("\n2. Checking PyMySQL:")
try:
    import pymysql
    print(f"   ✅ PyMySQL is installed (version: {pymysql.__version__})")
except ImportError:
    print("   ❌ PyMySQL is NOT installed!")
    print("      Run: pip3 install --user pymysql cryptography")

# 3. Attempt Connection
print("\n3. Testing MySQL Connection:")
if not mysql_password:
    print("   ⚠️  Skipping connection test (no password)")
else:
    config = {
        'host': 'ankitsharma6652.mysql.pythonanywhere-services.com',
        'user': 'ankitsharma6652',
        'password': mysql_password,
        'database': 'ankitsharma6652$mememaster',
        'connect_timeout': 10
    }
    
    try:
        conn = pymysql.connect(**config)
        print("   ✅ Connection SUCCESSFUL!")
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"      Server Version: {version[0]}")
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            table_names = [t[0] for t in tables]
            print(f"      Tables found: {', '.join(table_names) if table_names else 'None'}")
            
        conn.close()
    except Exception as e:
        print(f"   ❌ Connection FAILED: {e}")

print("\n" + "="*60)
