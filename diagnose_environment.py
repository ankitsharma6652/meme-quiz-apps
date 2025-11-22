import sys
import os
import platform

print("="*60)
print("🔍 DEEP DIAGNOSTIC: Environment & Database")
print("="*60)

# 1. Check Python Version
print(f"\n1. Python Version: {sys.version}")
print(f"   Platform: {platform.platform()}")
print(f"   Executable: {sys.executable}")

# 2. Check Environment Variables
print("\n2. Environment Variables:")
required_vars = ['PYTHONANYWHERE_DOMAIN', 'MYSQL_PASSWORD', 'MYSQL_USER', 'MYSQL_HOST', 'MYSQL_DB']
for var in required_vars:
    value = os.environ.get(var)
    status = "✅ Set" if value else "❌ Missing"
    masked_value = "*"*8 if value and 'PASSWORD' in var else value
    print(f"   {var:<25}: {status} ({masked_value})")

# 3. Check PyMySQL Installation
print("\n3. Checking PyMySQL Module:")
try:
    import pymysql
    print(f"   ✅ PyMySQL imported successfully!")
    print(f"   Location: {pymysql.__file__}")
    print(f"   Version: {pymysql.__version__}")
except ImportError as e:
    print(f"   ❌ PyMySQL Import FAILED: {e}")
    print("\n   DEBUG INFO: sys.path:")
    for p in sys.path:
        print(f"   - {p}")

# 4. Test Database Connection
print("\n4. Testing Database Connection:")
mysql_password = os.environ.get('MYSQL_PASSWORD')
if not mysql_password:
    print("   ⚠️  Skipping connection test (MYSQL_PASSWORD not set)")
else:
    try:
        conn = pymysql.connect(
            host='ankitsharma6652.mysql.pythonanywhere-services.com',
            user='ankitsharma6652',
            password=mysql_password,
            database='ankitsharma6652$mememaster',
            connect_timeout=5
        )
        print("   ✅ Connection SUCCESSFUL!")
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = [t[0] for t in cursor.fetchall()]
            print(f"   📊 Tables: {', '.join(tables)}")
        conn.close()
    except Exception as e:
        print(f"   ❌ Connection FAILED: {e}")

print("\n" + "="*60)
