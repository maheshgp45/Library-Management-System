import urllib.request
import urllib.parse

# Test student login
url = 'http://localhost:5000/login'
data = urllib.parse.urlencode({
    'username': 'student',
    'password': 'student123'
}).encode('utf-8')

print("Testing student login...")

try:
    req = urllib.request.Request(url, data=data, method='POST')
    with urllib.request.urlopen(req) as response:
        print(f"Login response status: {response.getcode()}")
        content = response.read().decode('utf-8')

        # Check if it redirects to user dashboard
        if 'user_dashboard' in content or 'Student Dashboard' in content:
            print("✅ SUCCESS: Student redirected to user dashboard")
        elif 'Invalid credentials' in content:
            print("❌ FAILED: Invalid credentials")
        elif 'Admin Dashboard' in content:
            print("❌ ERROR: Student redirected to admin dashboard")
        else:
            print("Response preview:", content[:200])

except Exception as e:
    print(f"Error: {e}")