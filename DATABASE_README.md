# Database Viewing Options

## When External People Ask to See Your Database

You now have multiple professional ways to show your database:

### 🎯 **BEST OPTION: Web Database Viewer**
1. Start your app: `python app.py`
2. Login as admin
3. Click "View Database" button
4. Shows beautiful formatted data with export options

### 💻 **Command Line Viewer**
- Run: `python view_database.py`
- Or: `view_database.bat` (Windows)
- Shows formatted terminal output

### 🖥️ **MongoDB Compass (GUI)**
- Download from mongodb.com
- Connect to: `mongodb://localhost:27017/library_management`
- Visual database browser

### 🐚 **MongoDB Shell**
```bash
mongosh "mongodb://localhost:27017/library_management"
db.books.find().pretty()
db.users.find().pretty()
db.issued_books.find().pretty()
```

### 📤 **Export Options**
- JSON export buttons in web viewer
- Download individual collections
- Share with external parties safely

## 🔒 Security Features
- Passwords automatically hidden
- ObjectIds converted to readable strings
- Admin-only access to database viewer
- Safe for demonstrations

## 🚀 Quick Start
```bash
# Web viewer (recommended)
python app.py

# Terminal viewer
python view_database.py

# Demo script
demo_database.bat
```