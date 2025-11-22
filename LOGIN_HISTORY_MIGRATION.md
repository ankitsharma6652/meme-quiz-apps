# LoginHistory Table Migration Guide

## Problem
After adding the LoginHistory table, the production database on PythonAnywhere needs to be updated.

## Solution
Run the migration script on PythonAnywhere to add the new table.

## Steps to Fix

### Option 1: Run via PythonAnywhere Bash Console (Recommended)

1. Go to PythonAnywhere Dashboard
2. Open a **Bash console**
3. Navigate to your project:
   ```bash
   cd ~/meme-quiz-apps
   ```

4. Run the migration script:
   ```bash
   python3 add_login_history_table.py
   ```

5. You should see:
   ```
   Adding LoginHistory table to database...
   ✅ LoginHistory table created successfully!
   Migration complete!
   ```

6. Reload your web app from the Web tab

### Option 2: Automatic on Next Deployment

The GitHub Action will deploy the migration script automatically. After deployment:

1. Go to PythonAnywhere Bash console
2. Run: `cd ~/meme-quiz-apps && python3 add_login_history_table.py`

## Verification

After running the migration, test by:
1. Sign out of your app
2. Sign in again with Google
3. The login should work without errors
4. Check the database to see login_history records

## What the Migration Does

- Creates the `login_history` table with columns:
  - `id` (Primary Key)
  - `user_email` (Foreign Key to user table)
  - `login_time` (Timestamp)
  - `ip_address` (User's IP)
  - `user_agent` (Browser info)
  - `login_method` (e.g., 'google')

- Does NOT affect existing `user` or `favorite` tables
- Safe to run multiple times (checks if table exists first)
