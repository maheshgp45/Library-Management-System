print("Starting HTTP test...")

import urllib.request
import urllib.parse
import http.cookiejar

print("Creating cookie jar...")

# Create a cookie jar to handle sessions
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

print("Preparing login data...")

# Login as admin
login_data = urllib.parse.urlencode({
    'username': 'admin',
    'password': 'admin123'
}).encode()

print("Attempting login...")

try:
    # First, login
    login_req = urllib.request.Request('http://localhost:5000/login', data=login_data, method='POST')
    login_req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    login_response = opener.open(login_req)
    print("Login status:", login_response.status)
    print("Login final URL:", login_response.url)

    # Check cookies
    print("Cookies after login:")
    for cookie in cj:
        print(f"  {cookie.name}: {cookie.value}")

    print("Accessing database viewer...")

    # Now access the database viewer
    db_req = urllib.request.Request('http://localhost:5000/admin/database')
    db_response = opener.open(db_req)
    print("Database viewer status:", db_response.status)
    print("Database viewer URL:", db_response.url)

    # Read a small portion of the response to verify it works
    content = db_response.read(300).decode()
    if "Database Viewer" in content:
        print("✅ SUCCESS: Database viewer is working correctly!")
        print("Response contains expected content.")
    else:
        print("❌ Unexpected response content")
        print("Content preview:", content[:200])

except Exception as e:
    print("Error:", str(e))
    import traceback
    traceback.print_exc()