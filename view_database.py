from models import *
import json

def display_database():
    print("=== LIBRARY MANAGEMENT SYSTEM DATABASE ===\n")

    # Display users
    print("👥 USERS:")
    users = get_all_users()
    for user in users:
        print(f"  ID: {user['_id']}")
        print(f"  Username: {user['username']}")
        print(f"  Role: {user['role']}")
        print("  ---")

    print("\n📚 BOOKS:")
    books = get_all_books()
    for book in books:
        print(f"  ID: {book['_id']}")
        print(f"  Title: {book['title']}")
        print(f"  Author: {book['author']}")
        print(f"  Category: {book['category']}")
        print(f"  Quantity: {book['quantity']}")
        print(f"  Available: {book['available']}")
        print("  ---")

    print("\n📖 ISSUED BOOKS:")
    issued_books = get_issued_books()
    if not issued_books:
        print("  No books currently issued")
    else:
        for issued in issued_books:
            print(f"  ID: {issued['_id']}")
            print(f"  User ID: {issued['user_id']}")
            print(f"  Book ID: {issued['book_id']}")
            print(f"  Issue Date: {issued['issue_date']}")
            print(f"  Return Date: {issued['return_date'] or 'Not returned'}")
            print("  ---")

if __name__ == "__main__":
    display_database()