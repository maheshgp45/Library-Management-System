from models import *

# Check what users exist
print("=== USERS IN DATABASE ===")
users = get_all_users()
for user in users:
    print(f"Username: {user['username']}, Role: {user['role']}")

print("\n=== BOOKS IN DATABASE ===")
books = get_all_books()
for book in books:
    print(f"Title: {book['title']}, Author: {book['author']}, Available: {book['available']}")

print("\n=== TESTING LOGIN ===")
# Test admin login
admin_user = find_user('admin')
if admin_user:
    print(f"Admin user found: {admin_user['username']}")
    print(f"Password hash: {admin_user['password']}")
    # Test password verification
    from werkzeug.security import check_password_hash
    is_valid = check_password_hash(admin_user['password'], 'admin123')
    print(f"Password 'admin123' valid: {is_valid}")
else:
    print("Admin user not found!")

# Test student login
student_user = find_user('student')
if student_user:
    print(f"Student user found: {student_user['username']}")
    is_valid = check_password_hash(student_user['password'], 'student123')
    print(f"Password 'student123' valid: {is_valid}")
else:
    print("Student user not found!")