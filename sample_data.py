from models import *

# Sample data
def insert_sample_data():
    # Create admin user
    if not find_user('admin'):
        create_user('admin', 'admin123', 'admin')

    # Create sample student
    if not find_user('student'):
        create_user('student', 'student123', 'student')

    # Add sample books
    sample_books = [
        {'title': 'Python Programming', 'author': 'John Doe', 'category': 'Programming', 'quantity': 5},
        {'title': 'Data Structures', 'author': 'Jane Smith', 'category': 'Computer Science', 'quantity': 3},
        {'title': 'Web Development', 'author': 'Bob Johnson', 'category': 'Programming', 'quantity': 4},
        {'title': 'Machine Learning', 'author': 'Alice Brown', 'category': 'AI', 'quantity': 2},
        {'title': 'Database Systems', 'author': 'Charlie Wilson', 'category': 'Computer Science', 'quantity': 3}
    ]

    for book in sample_books:
        # Check if book already exists
        existing = books_collection.find_one({'title': book['title']})
        if not existing:
            add_book(book['title'], book['author'], book['category'], book['quantity'])

if __name__ == '__main__':
    insert_sample_data()
    print('Sample data inserted successfully!')