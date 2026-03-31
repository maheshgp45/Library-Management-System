@echo off
echo ============================================
echo 📊 DATABASE VIEWING DEMO
echo ============================================
echo.
echo This demonstrates different ways to view your database:
echo.
echo 1. Web Interface (Recommended):
echo    - Run: python app.py
echo    - Login as admin
echo    - Click "View Database" button
echo.
echo 2. Command Line Viewer:
echo    - Run: python view_database.py
echo.
echo 3. MongoDB Shell:
echo    - Run: mongosh "mongodb://localhost:27017/library_management"
echo    - Then: db.books.find().pretty()
echo.
echo 4. MongoDB Compass GUI:
echo    - Download from: https://mongodb.com/try/download/compass
echo    - Connect to: mongodb://localhost:27017/library_management
echo.
echo Starting command line viewer...
echo.
python view_database.py
echo.
echo Demo completed! Press any key to exit...
pause > nul