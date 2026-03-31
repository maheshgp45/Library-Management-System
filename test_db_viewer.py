import sys
import os
sys.path.append(os.path.dirname(__file__))

from app import app, books_collection, users_collection, issued_books_collection

# Test the database collections directly
print("Testing database collections...")

try:
    books = list(books_collection.find())
    users = list(users_collection.find())
    issued_books = list(issued_books_collection.find())

    print(f"Books: {len(books)}")
    print(f"Users: {len(users)}")
    print(f"Issued Books: {len(issued_books)}")

    # Test the admin_dashboard function
    with app.test_request_context():
        from flask import session

        # Simulate admin login
        session['user_id'] = 'admin'
        session['role'] = 'admin'

        # Test the admin_dashboard function
        from app import admin_dashboard
        result = admin_dashboard()
        print("Admin dashboard executed successfully")
        print("Result type:", type(result))

except Exception as e:
    print("Error:", str(e))
    import traceback
    traceback.print_exc()