# 🚀 MySQL Setup Guide for PythonAnywhere

## Step 1: Create MySQL Database on PythonAnywhere

1. Go to **PythonAnywhere** → **Databases** tab
2. Set a MySQL password (if you haven't already)
3. Create a new database:
   - Database name will be: `ankitsharma6652$mememaster`
4. Note down your credentials:
   ```
   Host: ankitsharma6652.mysql.pythonanywhere-services.com
   Username: ankitsharma6652
   Password: [your-mysql-password]
   Database: ankitsharma6652$mememaster
   ```

---

## Step 2: Set Environment Variables on PythonAnywhere

1. Go to **Web** tab
2. Scroll to **Environment variables** section (or edit WSGI file)
3. Add these variables:

```bash
PYTHONANYWHERE_DOMAIN=ankitsharma6652.pythonanywhere.com
MYSQL_PASSWORD=your-mysql-password-here
MYSQL_USER=ankitsharma6652
MYSQL_HOST=ankitsharma6652.mysql.pythonanywhere-services.com
MYSQL_DB=ankitsharma6652$mememaster
```

**Alternative**: Edit `/var/www/ankitsharma6652_pythonanywhere_com_wsgi.py` and add:
```python
import os
os.environ['PYTHONANYWHERE_DOMAIN'] = 'ankitsharma6652.pythonanywhere.com'
os.environ['MYSQL_PASSWORD'] = 'your-mysql-password'
```

---

## Step 3: Install Dependencies

SSH into PythonAnywhere and run:

```bash
cd meme-quiz-apps
pip3 install --user pymysql cryptography
```

Or install from requirements.txt:
```bash
pip3 install --user -r requirements.txt
```

---

## Step 4: Migrate Existing Data (One-time)

If you have existing data in SQLite, migrate it to MySQL:

```bash
cd meme-quiz-apps

# Set your MySQL password
export MYSQL_PASSWORD='your-mysql-password'

# Run migration
python3 migrate_to_mysql.py
```

This will:
- ✅ Create tables in MySQL
- ✅ Copy all users from SQLite to MySQL
- ✅ Copy all favorites from SQLite to MySQL
- ✅ Handle duplicates automatically (upsert)

---

## Step 5: Update and Reload

```bash
cd meme-quiz-apps
git pull
```

Then go to **Web** tab and click **"Reload"**

---

## Step 6: Verify MySQL Connection

Check the error log after reload. You should see:
```
Using MySQL database: ankitsharma6652$mememaster
Database tables created!
```

If you see errors, check:
1. MySQL password is correct
2. Environment variables are set
3. PyMySQL is installed

---

## 🔄 Automatic Sync (Future Data)

Once MySQL is configured, the app will automatically:
- ✅ Use MySQL on PythonAnywhere
- ✅ Use SQLite on localhost
- ✅ All new users/favorites go directly to MySQL
- ✅ No manual syncing needed!

---

## 📊 Accessing MySQL Database

### Method 1: MySQL Console (PythonAnywhere)
```bash
mysql -u ankitsharma6652 -p -h ankitsharma6652.mysql.pythonanywhere-services.com ankitsharma6652\$mememaster
```

### Method 2: Python Script
```bash
cd meme-quiz-apps
python3 view_database.py
```

### Method 3: MySQL Workbench (Local)
1. Download MySQL Workbench
2. Create new connection:
   - Host: `ankitsharma6652.mysql.pythonanywhere-services.com`
   - Port: `3306`
   - Username: `ankitsharma6652`
   - Password: [your-password]
   - Database: `ankitsharma6652$mememaster`

---

## 🔍 Useful MySQL Commands

```sql
-- Show all tables
SHOW TABLES;

-- Count users
SELECT COUNT(*) FROM user;

-- Count favorites
SELECT COUNT(*) FROM favorite;

-- View recent users
SELECT * FROM user ORDER BY created_at DESC LIMIT 10;

-- View recent favorites
SELECT u.email, f.meme_title, f.created_at
FROM favorite f
JOIN user u ON f.user_id = u.id
ORDER BY f.created_at DESC
LIMIT 10;

-- Top users by favorites
SELECT u.email, u.name, COUNT(f.id) as favorite_count
FROM user u
LEFT JOIN favorite f ON u.id = f.user_id
GROUP BY u.id
ORDER BY favorite_count DESC
LIMIT 10;
```

---

## 🔧 Troubleshooting

### Error: "Access denied for user"
- Check MySQL password is correct
- Verify environment variable `MYSQL_PASSWORD` is set

### Error: "Unknown database"
- Database name must be: `ankitsharma6652$mememaster`
- Create it on PythonAnywhere Databases tab

### Error: "No module named 'pymysql'"
```bash
pip3 install --user pymysql cryptography
```

### App still using SQLite
- Ensure `PYTHONANYWHERE_DOMAIN` environment variable is set
- Check error logs for "Using MySQL database" message

---

## 📦 Backup MySQL Database

### Automatic Backup (Recommended)
Create a scheduled task on PythonAnywhere:
```bash
mysqldump -u ankitsharma6652 -p'your-password' -h ankitsharma6652.mysql.pythonanywhere-services.com ankitsharma6652\$mememaster > /home/ankitsharma6652/backups/mememaster_$(date +\%Y\%m\%d).sql
```

### Manual Backup
```bash
mysqldump -u ankitsharma6652 -p -h ankitsharma6652.mysql.pythonanywhere-services.com ankitsharma6652\$mememaster > backup.sql
```

### Restore from Backup
```bash
mysql -u ankitsharma6652 -p -h ankitsharma6652.mysql.pythonanywhere-services.com ankitsharma6652\$mememaster < backup.sql
```

---

## ✅ Checklist

- [ ] MySQL database created on PythonAnywhere
- [ ] MySQL password set
- [ ] Environment variables configured
- [ ] PyMySQL installed
- [ ] Data migrated from SQLite (if applicable)
- [ ] App reloaded
- [ ] MySQL connection verified in logs
- [ ] Test login and favorites work

---

## 🎯 Benefits of MySQL

1. **Better Performance** - Optimized for concurrent users
2. **Scalability** - Can handle more data and traffic
3. **Reliability** - Better for production environments
4. **Backup** - Easier to backup and restore
5. **Analytics** - Better query performance for statistics

---

## 📞 Quick Commands

```bash
# View database
python3 view_database.py

# Migrate data
export MYSQL_PASSWORD='your-password'
python3 migrate_to_mysql.py

# Check MySQL connection
mysql -u ankitsharma6652 -p -h ankitsharma6652.mysql.pythonanywhere-services.com

# Reload app
# Go to Web tab → Click "Reload"
```
