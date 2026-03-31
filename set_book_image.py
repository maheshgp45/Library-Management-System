"""
Script to add an image URL to a book directly in the database.
"""

from pymongo import MongoClient
from config import Config

# Connect to MongoDB
client = MongoClient(Config.MONGO_URI)
db = client[Config.DATABASE_NAME]
books_collection = db['books']

# Set image for Python Programming
result = books_collection.update_one(
    {'title': 'Python Programming'},
    {'$set': {'image': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=500&fit=crop'}}
)

if result.modified_count > 0:
    print("Image set for 'Python Programming'!")
else:
    print("Book not found!")

# Set image for Data Structures
result2 = books_collection.update_one(
    {'title': 'Data Structures'},
    {'$set': {'image': 'https://images.unsplash.com/photo-1516116216624-53e697fed8ce?w=400&h=500&fit=crop'}}
)

if result2.modified_count > 0:
    print("Image set for 'Data Structures'!")

print("\nDone! Restart the Flask app to see the images.")
