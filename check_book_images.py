"""
Script to check if book images are saved in the database.
"""

from pymongo import MongoClient
from config import Config

# Connect to MongoDB
client = MongoClient(Config.MONGO_URI)
db = client[Config.DATABASE_NAME]
books_collection = db['books']

def check_book_images():
    """Check all books and their image status."""
    books = list(books_collection.find())
    
    print(f"Total books: {len(books)}\n")
    
    for book in books:
        title = book.get('title', 'Unknown')
        book_id = str(book['_id'])
        image = book.get('image', None)
        
        print(f"Book: {title}")
        print(f"  ID: {book_id}")
        print(f"  Image field exists: {'Yes' if image is not None else 'No'}")
        if image:
            print(f"  Image URL: {image[:80]}..." if len(image) > 80 else f"  Image URL: {image}")
        print()

if __name__ == '__main__':
    check_book_images()
