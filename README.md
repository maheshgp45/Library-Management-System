# Library Management System

A complete Library Management System built with Flask, MongoDB, and HTML/CSS/JavaScript.

## Features

- User Authentication (Login/Signup)
- Role-based Access Control (Admin & Student)
- Admin Features:
  - Add, Update, Delete Books
  - View All Books and Issued Books
  - Manage Users
- Student/User Features:
  - View Available Books
  - Search Books by Title, Author, or Category
  - Issue and Return Books
  - View Issued Book History

## Tech Stack

- **Backend**: Python Flask
- **Database**: MongoDB
- **Frontend**: HTML, CSS, JavaScript
- **Security**: Password Hashing, Session-based Authentication

## Project Structure

```
library_management_system/
├── app.py                 # Main Flask application
├── models.py              # Database models and functions
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── sample_data.py         # Script to insert sample data
├── static/
│   ├── css/
│   │   └── style.css      # Stylesheet
│   └── js/
│       └── script.js      # JavaScript file
└── templates/
    ├── base.html          # Base template
    ├── login.html         # Login page
    ├── signup.html        # Signup page
    ├── admin_dashboard.html # Admin dashboard
    └── user_dashboard.html  # User dashboard
```

## Setup Instructions

### Prerequisites

1. Python 3.8 or higher
2. MongoDB installed and running
3. Git (optional)

### Installation

1. **Clone or Download the Project**
   ```
   cd your-workspace-directory
   # Copy the library_management_system folder
   ```

2. **Create Virtual Environment**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Configure MongoDB**
   - Make sure MongoDB is running on your system
   - Default connection: `mongodb://localhost:27017/library_management`
   - Update `config.py` if needed

5. **Insert Sample Data**
   ```
   python sample_data.py
   ```

6. **Run the Application**
   ```
   python app.py
   ```

7. **Access the Application**
   - Open your browser and go to `http://localhost:5000`
   - Login with:
     - Admin: username `admin`, password `admin123`
     - Student: username `student`, password `student123`

## Database Schema

### Users Collection
```json
{
  "_id": ObjectId,
  "username": "string",
  "password": "hashed_string",
  "role": "admin" | "student"
}
```

### Books Collection
```json
{
  "_id": ObjectId,
  "title": "string",
  "author": "string",
  "category": "string",
  "quantity": "number",
  "available": "number"
}
```

### Issued Books Collection
```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "book_id": ObjectId,
  "issue_date": "datetime",
  "return_date": "datetime" | null
}
```

## Usage

1. **Login/Signup**: Create an account or login with existing credentials
2. **Admin Dashboard**: Manage books, view issued books, and manage users
3. **User Dashboard**: Browse books, search, issue/return books

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control
- Input validation

## Contributing

This is a mini-project for educational purposes. Feel free to modify and extend the features.

## License

This project is for educational use only.