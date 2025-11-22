# 📊 Database Access Guide

## Database Location

Your MemeMaster app uses SQLite database stored in:
- **Local**: `mememaster.db` (in project root)
- **PythonAnywhere**: `/home/ankitsharma6652/meme-quiz-apps/mememaster.db`

## Database Schema

### Tables:
1. **user** - Stores user information
   - `id` (Primary Key)
   - `email` (Unique)
   - `name`
   - `picture` (Profile picture URL)
   - `created_at` (Timestamp)

2. **favorite** - Stores favorited memes
   - `id` (Primary Key)
   - `user_id` (Foreign Key → user.id)
   - `meme_id` (Unique meme identifier)
   - `meme_url` (URL of the meme)
   - `meme_title` (Title of the meme)
   - `created_at` (Timestamp)

---

## 🔧 Method 1: Using the Python Script (Easiest)

### On PythonAnywhere:
```bash
cd meme-quiz-apps
python3 view_database.py
```

### On Local:
```bash
cd /Users/ankit-sharma/Documents/meme-quiz-app
python3 view_database.py
```

This will show:
- All users
- All favorites
- Statistics (top users, total counts, etc.)

---

## 🔧 Method 2: Using SQLite Command Line

### On PythonAnywhere:
```bash
cd meme-quiz-apps
sqlite3 mememaster.db
```

### On Local (if database exists):
```bash
cd /Users/ankit-sharma/Documents/meme-quiz-app
sqlite3 mememaster.db
```

### Useful SQLite Commands:
```sql
-- List all tables
.tables

-- View table structure
.schema user
.schema favorite

-- View all users
SELECT * FROM user;

-- View all favorites
SELECT * FROM favorite;

-- Count users
SELECT COUNT(*) FROM user;

-- Count favorites per user
SELECT u.email, u.name, COUNT(f.id) as favorite_count
FROM user u
LEFT JOIN favorite f ON u.id = f.user_id
GROUP BY u.id
ORDER BY favorite_count DESC;

-- View recent favorites
SELECT u.email, f.meme_title, f.created_at
FROM favorite f
JOIN user u ON f.user_id = u.id
ORDER BY f.created_at DESC
LIMIT 10;

-- Exit SQLite
.quit
```

---

## 🔧 Method 3: Using DB Browser for SQLite (GUI)

1. **Download**: https://sqlitebrowser.org/
2. **Install** DB Browser for SQLite
3. **Open Database**:
   - For PythonAnywhere: Download `mememaster.db` first
   - For Local: Open `/Users/ankit-sharma/Documents/meme-quiz-app/mememaster.db`
4. **Browse Data** using the GUI

---

## 🔧 Method 4: Download Database from PythonAnywhere

### Using SCP:
```bash
scp ankitsharma6652@ssh.pythonanywhere.com:meme-quiz-apps/mememaster.db ./mememaster_backup.db
```

### Using PythonAnywhere Web Interface:
1. Go to **Files** tab
2. Navigate to `/home/ankitsharma6652/meme-quiz-apps/`
3. Click on `mememaster.db`
4. Click **Download**

---

## 📊 Export Data to CSV

Create a Python script to export data:

```python
import sqlite3
import csv

conn = sqlite3.connect('mememaster.db')
cursor = conn.cursor()

# Export users
cursor.execute("SELECT * FROM user")
with open('users.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Email', 'Name', 'Picture', 'Created'])
    writer.writerows(cursor.fetchall())

# Export favorites
cursor.execute("SELECT * FROM favorite")
with open('favorites.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'UserID', 'MemeID', 'MemeURL', 'MemeTitle', 'Created'])
    writer.writerows(cursor.fetchall())

conn.close()
print("✅ Data exported to users.csv and favorites.csv")
```

---

## 🔒 Database Backup

### Automatic Backup Script:
```bash
#!/bin/bash
# backup_db.sh
DATE=$(date +%Y%m%d_%H%M%S)
cp mememaster.db backups/mememaster_$DATE.db
echo "✅ Backup created: backups/mememaster_$DATE.db"
```

### On PythonAnywhere (scheduled task):
```bash
cd /home/ankitsharma6652/meme-quiz-apps && cp mememaster.db backups/mememaster_$(date +\%Y\%m\%d).db
```

---

## 🚨 Important Notes

1. **Never edit the database while the app is running** - it can cause corruption
2. **Always backup before making changes**
3. **Use transactions** when modifying data
4. **The database file is in .gitignore** - it won't be committed to Git

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| View all data | `python3 view_database.py` |
| Open SQLite CLI | `sqlite3 mememaster.db` |
| Count users | `SELECT COUNT(*) FROM user;` |
| Count favorites | `SELECT COUNT(*) FROM favorite;` |
| Backup database | `cp mememaster.db mememaster_backup.db` |
| Download from PA | Use Files tab or SCP |
