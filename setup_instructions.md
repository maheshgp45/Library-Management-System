# Step-by-Step Setup Instructions

## 1. Install Python

Download and install Python 3.8 or higher from https://python.org

Verify installation:
```
python --version
```

## 2. Install MongoDB

### Windows:
1. Download MongoDB Community Server from https://mongodb.com
2. Install MongoDB
3. Start MongoDB service or run `mongod` from command prompt

### Linux/Mac:
Use package manager or download from official site

## 3. Set Up the Project

1. Navigate to the project directory:
   ```
   cd library_management_system
   ```

2. Create virtual environment:
   ```
   python -m venv venv
   ```

3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## 4. Configure the Application

1. Ensure MongoDB is running
2. Update `config.py` if your MongoDB connection string is different
3. Run sample data script:
   ```
   python sample_data.py
   ```

## 5. Run the Application

```
python app.py
```

The application will start on `http://localhost:5000`

## 6. Access the Application

- Open browser and go to `http://localhost:5000`
- Login with sample accounts:
  - Admin: `admin` / `admin123`
  - Student: `student` / `student123`

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running
- Check if port 27017 is available
- Update MONGO_URI in config.py

### Import Errors
- Make sure all dependencies are installed
- Check Python version compatibility

### Port Already in Use
- Change the port in app.py: `app.run(debug=True, port=5001)`

## Development

To run in development mode with auto-reload:
```
FLASK_ENV=development python app.py
```

---

# 📊 Database Viewing Guide

## How to Show Database to External People

When someone asks to see your database, you have several options depending on what you want to show them:

### 🌐 Option 1: Web Interface (Recommended for Demos)
1. **Run your Flask application:**
   ```bash
   python app.py
   ```

2. **Login as Admin** and click "View Database" button in the admin dashboard

3. **Show them the Database Viewer page** which displays:
   - All books with details
   - All users (passwords hidden for security)
   - All issued books with relationships

### 💻 Option 2: Command Line Viewer
1. **Run the database viewer script:**
   ```bash
   python view_database.py
   ```
   Or double-click `view_database.bat` on Windows

2. **This shows formatted output** of all collections in the terminal

### 🖥️ Option 3: MongoDB Compass (GUI Tool)
1. **Download MongoDB Compass** from https://www.mongodb.com/try/download/compass

2. **Connect to your database:**
   - Connection String: `mongodb://localhost:27017/library_management`
   - Or use your custom MongoDB URI from `config.py`

3. **Show collections:**
   - `books` - All book information
   - `users` - User accounts (passwords are hashed)
   - `issued_books` - Borrowing records

### 🐚 Option 4: MongoDB Shell
1. **Open command prompt/terminal**

2. **Connect to MongoDB:**
   ```bash
   mongosh "mongodb://localhost:27017/library_management"
   ```

3. **View collections:**
   ```javascript
   // Show all books
   db.books.find().pretty()

   // Show all users
   db.users.find().pretty()

   // Show issued books
   db.issued_books.find().pretty()

   // Count documents
   db.books.count()
   db.users.count()
   db.issued_books.count()
   ```

### 📤 Option 5: Export Data as JSON
Use the "Export" buttons in the web Database Viewer to download JSON files of each collection.

## 🔒 Security Notes:
- **Passwords are hidden** in the web interface for security
- **Never share actual password hashes** with external people
- **ObjectIds are converted to strings** for readability
- **Use admin access only** for database viewing

## 🚀 Quick Demo Commands:
```bash
# Start the web app
python app.py

# View database in terminal
python view_database.py

# Connect with MongoDB shell
mongosh "mongodb://localhost:27017/library_management"
```