"""
Script to remove all book cover images from the database.
Run this to start fresh and add your own images.
"""

from pymongo import MongoClient
from config import Config

# Connect to MongoDB
client = MongoClient(Config.MONGO_URI)
db = client[Config.DATABASE_NAME]
books_collection = db['books']

def remove_all_images():
    """Remove image field from all books."""
    result = books_collection.update_many(
        {},
        {'$unset': {'image': ''}}
    )
    print(f"Removed images from {result.modified_count} books.")

if __name__ == '__main__':
    remove_all_images()
    print("Done! All book images have been removed.")
    print("You can now add your own images using the admin panel.")
