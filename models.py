from pymongo import MongoClient
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

client = MongoClient(Config.MONGO_URI)
db = client[Config.DATABASE_NAME]

# Collections
users_collection = db['users']
books_collection = db['books']
issued_books_collection = db['issued_books']
reviews_collection = db['reviews']
wishlist_collection = db['wishlist']
pending_requests_collection = db['pending_requests']

# Default settings
DEFAULT_BORROW_DAYS = 14  # Days before due
FINE_PER_DAY = 5  # Fine per day for late return

# User functions
def create_user(username, password, role='student'):
    hashed_password = generate_password_hash(password)
    user = {
        'username': username,
        'password': hashed_password,
        'role': role,
        'profile_image': '/static/uploads/profile/default_profile.svg',
        'email': '',
        'phone': '',
        'address': '',
        'date_of_birth': None,
        'bio': '',
        'department': '',
        'year': '',
        'created_at': datetime.now()
    }
    users_collection.insert_one(user)

def find_user(username):
    return users_collection.find_one({'username': username})

def verify_password(user, password):
    return check_password_hash(user['password'], password)

# Book functions
def add_book(title, author, category, quantity, image=None, description='', isbn='', publisher='', published_year=None):
    # Use default placeholder if no image provided
    if image is None:
        image = '/static/uploads/book_covers/placeholder.svg'
    book = {
        'title': title,
        'author': author,
        'category': category,
        'quantity': quantity,
        'available': quantity,
        'image': image,
        'description': description,
        'isbn': isbn,
        'publisher': publisher,
        'published_year': published_year,
        'rating': 0,
        'rating_count': 0,
        'created_at': datetime.now()
    }
    books_collection.insert_one(book)

def get_all_books():
    return list(books_collection.find())

def find_book(book_id):
    from bson import ObjectId
    return books_collection.find_one({'_id': ObjectId(book_id)})

def update_book(book_id, title, author, category, quantity, image=None, description='', isbn='', publisher='', published_year=None):
    from bson import ObjectId
    update_data = {
        'title': title, 
        'author': author, 
        'category': category, 
        'quantity': quantity,
        'description': description,
        'isbn': isbn,
        'publisher': publisher,
        'published_year': published_year
    }
    if image is not None:
        update_data['image'] = image
    books_collection.update_one(
        {'_id': ObjectId(book_id)},
        {'$set': update_data}
    )

def update_book_image(book_id, image):
    from bson import ObjectId
    books_collection.update_one(
        {'_id': ObjectId(book_id)},
        {'$set': {'image': image}}
    )

def delete_book(book_id):
    from bson import ObjectId
    books_collection.delete_one({'_id': ObjectId(book_id)})

def delete_user(user_id):
    from bson import ObjectId
    users_collection.delete_one({'_id': ObjectId(user_id)})

def search_books(query, category_filter=None, author_filter=None):
    search_query = {
        '$or': [
            {'title': {'$regex': query, '$options': 'i'}},
            {'author': {'$regex': query, '$options': 'i'}},
            {'category': {'$regex': query, '$options': 'i'}},
            {'isbn': {'$regex': query, '$options': 'i'}}
        ]
    }
    
    if category_filter and category_filter != 'all':
        search_query['category'] = category_filter
    
    if author_filter:
        search_query['author'] = {'$regex': author_filter, '$options': 'i'}
    
    return list(books_collection.find(search_query))

def get_books_by_category(category):
    return list(books_collection.find({'category': category}))

def get_all_categories():
    categories = books_collection.distinct('category')
    return categories

# Pending book request functions
def create_pending_request(user_id, book_id):
    """Create a pending request for a book"""
    from bson import ObjectId
    # Check if already requested
    existing = pending_requests_collection.find_one({
        'user_id': ObjectId(user_id),
        'book_id': ObjectId(book_id),
        'status': 'pending'
    })
    if existing:
        return False
    
    request = {
        'user_id': ObjectId(user_id),
        'book_id': ObjectId(book_id),
        'request_date': datetime.now(),
        'status': 'pending'
    }
    pending_requests_collection.insert_one(request)
    return True

def get_pending_requests(user_id=None):
    """Get pending book requests for a user"""
    from bson import ObjectId
    query = {'status': 'pending'}
    if user_id:
        query['user_id'] = ObjectId(user_id)
    
    requests = list(pending_requests_collection.find(query).sort('request_date', -1))
    
    # Enrich with book details
    enriched = []
    for req in requests:
        book = books_collection.find_one({'_id': req['book_id']})
        user = users_collection.find_one({'_id': req['user_id']})
        if book:
            enriched.append({
                '_id': str(req['_id']),
                'user_id': str(req['user_id']),
                'book_id': str(req['book_id']),
                'request_date': req['request_date'],
                'status': req['status'],
                'book_title': book['title'],
                'book_author': book['author'],
                'book_image': book['image'],
                'user_name': user['username'] if user else 'Unknown'
            })
    
    return enriched

def approve_pending_request(request_id):
    """Approve a pending request and issue the book"""
    from bson import ObjectId
    pending_req = pending_requests_collection.find_one({'_id': ObjectId(request_id)})
    
    if not pending_req or pending_req['status'] != 'pending':
        return False
    
    # Check if book is still available
    book = books_collection.find_one({'_id': pending_req['book_id']})
    if not book or book['available'] <= 0:
        pending_requests_collection.update_one(
            {'_id': ObjectId(request_id)},
            {'$set': {'status': 'rejected', 'rejection_reason': 'Book no longer available'}}
        )
        return False
    
    # Issue the book
    due_date = datetime.now() + timedelta(days=DEFAULT_BORROW_DAYS)
    issued_book = {
        'user_id': pending_req['user_id'],
        'book_id': pending_req['book_id'],
        'issue_date': datetime.now(),
        'due_date': due_date,
        'return_date': None,
        'fine': 0,
        'status': 'issued'
    }
    issued_books_collection.insert_one(issued_book)
    
    # Decrease available count
    books_collection.update_one(
        {'_id': pending_req['book_id']},
        {'$inc': {'available': -1}}
    )
    
    # Update pending request status
    pending_requests_collection.update_one(
        {'_id': ObjectId(request_id)},
        {'$set': {'status': 'approved', 'approved_date': datetime.now()}}
    )
    
    return True

def reject_pending_request(request_id):
    """Reject a pending request"""
    from bson import ObjectId
    pending_requests_collection.update_one(
        {'_id': ObjectId(request_id)},
        {'$set': {'status': 'rejected', 'rejection_date': datetime.now()}}
    )
    return True

def cancel_pending_request(user_id, book_id):
    """Cancel a pending request by user"""
    from bson import ObjectId
    pending_requests_collection.delete_one({
        'user_id': ObjectId(user_id),
        'book_id': ObjectId(book_id),
        'status': 'pending'
    })
    return True

# Issued books functions with due dates
def issue_book(user_id, book_id):
    """Issue a book to a user immediately"""
    from bson import ObjectId
    book = find_book(book_id)
    if book and book['available'] > 0:
        due_date = datetime.now() + timedelta(days=DEFAULT_BORROW_DAYS)
        issued_book = {
            'user_id': ObjectId(user_id),
            'book_id': ObjectId(book_id),
            'issue_date': datetime.now(),
            'due_date': due_date,
            'return_date': None,
            'fine': 0,
            'status': 'issued'
        }
        issued_books_collection.insert_one(issued_book)
        books_collection.update_one(
            {'_id': ObjectId(book_id)},
            {'$inc': {'available': -1}}
        )
        return True
    return False

def return_book(user_id, book_id):
    from bson import ObjectId
    try:
        # Handle both string and ObjectId
        if isinstance(book_id, str):
            book_id = ObjectId(book_id)
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        
        # First try to find book that hasn't been returned yet (return_date is None)
        issued_book = issued_books_collection.find_one({
            'user_id': user_id,
            'book_id': book_id,
            'return_date': None
        })
        
        # If not found, try to find any book with this user_id and book_id that might have return_date set
        if not issued_book:
            issued_book = issued_books_collection.find_one({
                'user_id': user_id,
                'book_id': book_id
            })
            
        if issued_book:
            # Check if already returned
            if issued_book.get('return_date') and issued_book.get('status') == 'returned':
                return 'already_returned'
            
            # Calculate fine if late
            return_date = datetime.now()
            due_date = issued_book.get('due_date')
            fine = 0
            if due_date and return_date > due_date:
                days_late = (return_date - due_date).days
                fine = days_late * FINE_PER_DAY
            
            # Update the record
            issued_books_collection.update_one(
                {'_id': issued_book['_id']},
                {'$set': {
                    'return_date': return_date,
                    'fine': fine,
                    'status': 'returned'
                }}
            )
            # Increase available count
            books_collection.update_one(
                {'_id': book_id},
                {'$inc': {'available': 1}}
            )
            return fine  # Return the fine amount
        return False
    except Exception as e:
        print(f"Error in return_book: {e}")
        return False

def calculate_fine(issued_book):
    """Calculate fine for an issued book"""
    if issued_book.get('return_date'):
        return issued_book.get('fine', 0)
    
    due_date = issued_book.get('due_date')
    if due_date and datetime.now() > due_date:
        days_late = (datetime.now() - due_date).days
        return days_late * FINE_PER_DAY
    return 0

def get_issued_books(user_id=None):
    from bson import ObjectId
    query = {} if user_id is None else {'user_id': ObjectId(user_id)}
    issued_books = list(issued_books_collection.find(query).sort('issue_date', -1))
    
    # Enrich with book and user details
    enriched_issued_books = []
    for issued in issued_books:
        book = books_collection.find_one({'_id': issued['book_id']})
        user = users_collection.find_one({'_id': issued['user_id']})
        
        # Calculate fine if not returned
        fine = calculate_fine(issued) if not issued.get('return_date') else issued.get('fine', 0)
        
        # Determine status based on return_date and due_date
        if issued.get('return_date'):
            status = 'returned'
        elif issued.get('due_date') and issued.get('due_date') < datetime.now():
            status = 'overdue'
        else:
            status = 'issued'
        
        enriched = {
            '_id': issued['_id'],
            'user_id': issued['user_id'],
            'book_id': issued['book_id'],
            'issue_date': issued['issue_date'],
            'due_date': issued.get('due_date'),
            'return_date': issued.get('return_date'),
            'fine': fine,
            'status': status,
            'book_title': book['title'] if book else 'Unknown Book',
            'book_author': book['author'] if book else 'Unknown',
            'book_image': book['image'] if book else '',
            'user_name': user['username'] if user else 'Unknown User'
        }
        enriched_issued_books.append(enriched)
    
    return enriched_issued_books

def get_overdue_books():
    """Get all overdue books"""
    from bson import ObjectId
    current_date = datetime.now()
    overdue = list(issued_books_collection.find({
        'return_date': None,
        'due_date': {'$lt': current_date}
    }))
    
    enriched = []
    for issued in overdue:
        book = books_collection.find_one({'_id': issued['book_id']})
        user = users_collection.find_one({'_id': issued['user_id']})
        days_overdue = (current_date - issued['due_date']).days
        fine = days_overdue * FINE_PER_DAY
        
        enriched.append({
            '_id': issued['_id'],
            'book_title': book['title'] if book else 'Unknown',
            'user_name': user['username'] if user else 'Unknown',
            'due_date': issued['due_date'],
            'days_overdue': days_overdue,
            'fine': fine
        })
    
    return enriched

# Reviews functions
def add_review(book_id, user_id, rating, comment):
    from bson import ObjectId
    review = {
        'book_id': ObjectId(book_id),
        'user_id': ObjectId(user_id),
        'rating': rating,
        'comment': comment,
        'created_at': datetime.now()
    }
    reviews_collection.insert_one(review)
    
    # Update book's average rating
    update_book_rating(book_id)

def get_book_reviews(book_id):
    from bson import ObjectId
    reviews = list(reviews_collection.find({'book_id': ObjectId(book_id)}).sort('created_at', -1))
    
    enriched = []
    for review in reviews:
        user = users_collection.find_one({'_id': review['user_id']})
        enriched.append({
            '_id': review['_id'],
            'rating': review['rating'],
            'comment': review['comment'],
            'created_at': review['created_at'],
            'user_name': user['username'] if user else 'Unknown'
        })
    
    return enriched

def update_book_rating(book_id):
    from bson import ObjectId
    reviews = list(reviews_collection.find({'book_id': ObjectId(book_id)}))
    
    if reviews:
        total_rating = sum(r['rating'] for r in reviews)
        avg_rating = total_rating / len(reviews)
        books_collection.update_one(
            {'_id': ObjectId(book_id)},
            {'$set': {'rating': round(avg_rating, 1), 'rating_count': len(reviews)}}
        )

# Wishlist functions
def add_to_wishlist(user_id, book_id):
    from bson import ObjectId
    # Check if already in wishlist
    existing = wishlist_collection.find_one({
        'user_id': ObjectId(user_id),
        'book_id': ObjectId(book_id)
    })
    if not existing:
        wishlist = {
            'user_id': ObjectId(user_id),
            'book_id': ObjectId(book_id),
            'added_at': datetime.now()
        }
        wishlist_collection.insert_one(wishlist)
        return True
    return False

def remove_from_wishlist(user_id, book_id):
    from bson import ObjectId
    wishlist_collection.delete_one({
        'user_id': ObjectId(user_id),
        'book_id': ObjectId(book_id)
    })

def get_wishlist(user_id):
    from bson import ObjectId
    wishlist = list(wishlist_collection.find({'user_id': ObjectId(user_id)}))
    
    enriched = []
    for item in wishlist:
        book = books_collection.find_one({'_id': item['book_id']})
        if book:
            enriched.append({
                '_id': item['_id'],
                'book_id': item['book_id'],
                'added_at': item['added_at'],
                'book': book
            })
    
    return enriched

def is_in_wishlist(user_id, book_id):
    from bson import ObjectId
    return wishlist_collection.find_one({
        'user_id': ObjectId(user_id),
        'book_id': ObjectId(book_id)
    }) is not None

# User functions
def get_all_users():
    return list(users_collection.find())

def update_user_profile_image(user_id, profile_image):
    from bson import ObjectId
    users_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'profile_image': profile_image}}
    )

def get_user_by_id(user_id):
    from bson import ObjectId
    return users_collection.find_one({'_id': ObjectId(user_id)})

def update_user_profile(user_id, email=None, phone=None, address=None, date_of_birth=None, bio=None, department=None, year=None):
    from bson import ObjectId
    update_data = {}
    if email is not None:
        update_data['email'] = email
    if phone is not None:
        update_data['phone'] = phone
    if address is not None:
        update_data['address'] = address
    if date_of_birth is not None:
        update_data['date_of_birth'] = date_of_birth
    if bio is not None:
        update_data['bio'] = bio
    if department is not None:
        update_data['department'] = department
    if year is not None:
        update_data['year'] = year
    
    if update_data:
        users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})

# Statistics functions
def get_library_stats():
    total_books = books_collection.count_documents({})
    total_users = users_collection.count_documents({})
    total_issued = issued_books_collection.count_documents({'return_date': None})
    total_returned = issued_books_collection.count_documents({'return_date': {'$ne': None}})
    
    # Calculate total fines
    all_issued = list(issued_books_collection.find({'return_date': {'$ne': None}}))
    total_fines = sum(issued.get('fine', 0) for issued in all_issued)
    
    # Get overdue count
    overdue_count = len(get_overdue_books())
    
    return {
        'total_books': total_books,
        'total_users': total_users,
        'total_issued': total_issued,
        'total_returned': total_returned,
        'total_fines': total_fines,
        'overdue_count': overdue_count
    }

def get_borrowing_history(user_id):
    """Get complete borrowing history for a user"""
    from bson import ObjectId
    history = list(issued_books_collection.find({'user_id': ObjectId(user_id)}).sort('issue_date', -1))
    
    enriched = []
    for issued in history:
        book = books_collection.find_one({'_id': issued['book_id']})
        enriched.append({
            '_id': issued['_id'],
            'issue_date': issued['issue_date'],
            'due_date': issued.get('due_date'),
            'return_date': issued.get('return_date'),
            'fine': issued.get('fine', 0),
            'status': issued.get('status', 'unknown'),
            'book_title': book['title'] if book else 'Unknown',
            'book_author': book['author'] if book else 'Unknown',
            'book_image': book['image'] if book else ''
        })
    
    return enriched

def get_returned_books():
    """Get all books that have been returned (available for borrowing)"""
    # Get all returned books from issued_books collection
    returned_records = list(issued_books_collection.find({'status': 'returned'}).sort('return_date', -1))
    
    # Get all currently available books (these are also available for borrowing)
    available_books = list(books_collection.find({'available': {'$gt': 0}}))
    
    # Create a set of book IDs that have been returned
    returned_book_ids = set()
    for record in returned_records:
        returned_book_ids.add(record['book_id'])
    
    # Enrich with who returned the book and when
    enriched_returned = []
    for record in returned_records:
        book = books_collection.find_one({'_id': record['book_id']})
        user = users_collection.find_one({'_id': record['user_id']})
        if book:
            enriched_returned.append({
                '_id': record['_id'],
                'book_id': record['book_id'],
                'book_title': book['title'],
                'book_author': book['author'],
                'book_image': book['image'],
                'book_category': book.get('category', ''),
                'book_description': book.get('description', ''),
                'returned_by': user['username'] if user else 'Unknown',
                'return_date': record.get('return_date'),
                'was_available': book.get('available', 0)
            })
    
    return enriched_returned
