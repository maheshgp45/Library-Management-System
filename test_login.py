from models import find_user, verify_password

def test_login(username, password):
    print(f"Testing login for: {username}")
    user = find_user(username)
    if user:
        print(f"User found: {user['username']}, Role: {user['role']}")
        is_valid = verify_password(user, password)
        print(f"Password valid: {is_valid}")
        return is_valid
    else:
        print("User not found!")
        return False

# Test cases
print("=== LOGIN TESTS ===")
test_login('admin', 'admin123')
print()
test_login('student', 'student123')
print()
test_login('admin', 'wrongpassword')
print()
test_login('nonexistent', 'password')