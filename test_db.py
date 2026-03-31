from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import sys

try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    # Test the connection
    client.admin.command('ping')
    print("✅ MongoDB is running and accessible!")
    print("Connection successful to:", client.server_info()['version'])

    # Test our database
    db = client['library_management']
    print("✅ Database 'library_management' is accessible!")

    # Check collections
    collections = db.list_collection_names()
    print("Existing collections:", collections)

except ConnectionFailure:
    print("❌ Cannot connect to MongoDB!")
    print("Please make sure MongoDB is installed and running.")
    print("Download from: https://www.mongodb.com/try/download/community")
    sys.exit(1)
except Exception as e:
    print("❌ Error:", str(e))
    sys.exit(1)