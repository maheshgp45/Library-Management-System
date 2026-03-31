"""
Script to add sample book cover images to existing books.
This script updates books with placeholder images based on their titles.
"""

from pymongo import MongoClient
from config import Config

# Connect to MongoDB
client = MongoClient(Config.MONGO_URI)
db = client[Config.DATABASE_NAME]
books_collection = db['books']

# Local placeholder image
DEFAULT_COVER = '/static/uploads/book_covers/placeholder.svg'


def get_cover_for_book(title, author, category):
    """Determine the best cover image URL for a book based on its content."""
    search_text = f"{title} {author} {category}".lower()
    
    # Return default book cover image
    return DEFAULT_COVER


def add_sample_images():
    """Add sample images to all books that don't have images."""
    books = list(books_collection.find({'image': {'$exists': False}}))
    
    count = 0
    for book in books:
        title = book.get('title', '')
        author = book.get('author', '')
        category = book.get('category', '')
        
        image_url = get_cover_for_book(title, author, category)
        
        books_collection.update_one(
            {'_id': book['_id']},
            {'$set': {'image': image_url}}
        )
        
        count += 1
        print(f"Added image to: {title}")
    
    print(f"\nTotal books updated: {count}")
    return count


def update_all_images():
    """Update all books with sample images (overwrites existing)."""
    books = list(books_collection.find())
    
    count = 0
    for book in books:
        title = book.get('title', '')
        author = book.get('author', '')
        category = book.get('category', '')
        
        image_url = get_cover_for_book(title, author, category)
        
        books_collection.update_one(
            {'_id': book['_id']},
            {'$set': {'image': image_url}}
        )
        
        count += 1
        print(f"Updated image for: {title}")
    
    print(f"\nTotal books updated: {count}")
    return count


if __name__ == '__main__':
    print("=" * 50)
    print("Sample Book Cover Image Adder")
    print("=" * 50)
    print("\nAdding sample book cover images to all books...")
    
    # Automatically update all books
    update_all_images()
    
    print("\nDone! Sample images have been added to all books.")
