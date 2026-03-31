import urllib.request
import urllib.parse
import sys

print("Testing login endpoint...")

# Test the login endpoint
url = 'http://localhost:5000/login'
data = urllib.parse.urlencode({
    'username': 'admin',
    'password': 'admin123'
}).encode('utf-8')

print(f"Sending POST request to {url}")
print(f"Data: username=admin, password=admin123")

try:
    req = urllib.request.Request(url, data=data, method='POST')
    print("Request created, opening connection...")
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.getcode()}")
        print(f"Response Headers: {dict(response.headers)}")
        content = response.read().decode('utf-8')
        print(f"Response contains: {len(content)} characters")
        # Look for specific content
        if 'Invalid credentials' in content:
            print("❌ LOGIN FAILED: Invalid credentials message found")
        elif 'Login successful' in content:
            print("✅ LOGIN SUCCESSFUL")
        elif 'redirect' in content.lower():
            print("✅ LOGIN SUCCESSFUL (redirect detected)")
        else:
            print("Response preview:", content[:200])

except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    content = e.read().decode('utf-8')
    print(f"Error Response: {content[:500]}")
    if 'Invalid credentials' in content:
        print("❌ LOGIN FAILED: Invalid credentials")
except urllib.error.URLError as e:
    print(f"URL Error: {e}")
    print("Cannot connect to Flask app. Is it running on port 5000?")
except Exception as e:
    print(f"Unexpected Error: {e}")
    import traceback
    traceback.print_exc()