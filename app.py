from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import *
from bson import ObjectId
import os

app = Flask(__name__)
app.config.from_object('config.Config')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configure upload folder for book images
UPLOAD_FOLDER = os.path.join('static', 'uploads', 'book_covers')
PROFILE_UPLOAD_FOLDER = os.path.join('static', 'uploads', 'profile')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Removed PDF - only actual images allowed
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROFILE_UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file, book_id):
    if file and allowed_file(file.filename):
        # Get the original file extension
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext == 'jpeg':
            ext = 'jpg'
        filename = f"book_{book_id}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return f"/static/uploads/book_covers/{filename}"
    return None

def save_profile_image(file, user_id):
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"profile_{user_id}.{ext}"
        filepath = os.path.join(PROFILE_UPLOAD_FOLDER, filename)
        file.save(filepath)
        return f"/static/uploads/profile/{filename}"
    return None

@app.route('/')
def index():
    if 'user_id' in session:
        user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
        if user['role'] == 'admin':
            return redirect(url_for('admin_dashboard_modern'))
        else:
            return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_type = request.form.get('login_type', 'student')  # Default to student
        
        user = find_user(username)
        if user and verify_password(user, password):
            # Check if the login type matches the user's role
            user_role = user.get('role', 'student')
            
            if login_type == 'admin' and user_role != 'admin':
                flash('Please use Admin Login for administrator accounts', 'error')
                return render_template('login.html')
            elif login_type == 'student' and user_role == 'admin':
                flash('Please use Admin Login for administrator accounts', 'error')
                return render_template('login.html')
            
            session['user_id'] = str(user['_id'])
            session['role'] = user_role
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'student')
        if find_user(username):
            flash('Username already exists', 'error')
        else:
            create_user(username, password, role)
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/upload_profile', methods=['POST'])
def upload_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'profile_image' in request.files:
        image_file = request.files['profile_image']
        if image_file and image_file.filename:
            saved_url = save_profile_image(image_file, session['user_id'])
            if saved_url:
                update_user_profile_image(session['user_id'], saved_url)
                flash('Profile image updated!', 'success')
    
    # Redirect back to the appropriate dashboard
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard_modern'))
    else:
        return redirect(url_for('user_dashboard'))

@app.route('/profile/update', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    address = request.form.get('address', '')
    date_of_birth = request.form.get('date_of_birth', '')
    bio = request.form.get('bio', '')
    department = request.form.get('department', '')
    
    # Only get year for students, not for admins
    year = None
    if session.get('role') != 'admin':
        year = request.form.get('year', '')
    
    update_user_profile(session['user_id'], email, phone, address, date_of_birth, bio, department, year)
    flash('Profile updated successfully!', 'success')
    
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('user_dashboard'))

@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    books = get_all_books()
    issued_books = get_issued_books()
    users = get_all_users()
    current_user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
    return render_template('admin_dashboard.html', books=books, issued_books=issued_books, users=users, current_user=current_user)

@app.route('/admin/modern')
def admin_dashboard_modern():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    books = get_all_books()
    issued_books = get_issued_books()
    users = get_all_users()
    current_user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
    # Calculate returned books (issued books that have been returned)
    returned_books = len([i for i in issued_books if i.get('return_date')])
    return render_template('admin_dashboard_modern.html', books=books, issued_books=issued_books, users=users, current_user=current_user, returned_books=returned_books)

@app.route('/admin/search', methods=['GET', 'POST'])
def admin_search_route():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        query = request.form.get('query', '')
    else:
        query = request.args.get('query', '')
    
    if query:
        books = search_books(query)
    else:
        books = get_all_books()
    
    issued_books = get_issued_books()
    users = get_all_users()
    return render_template('admin_dashboard.html', books=books, issued_books=issued_books, users=users, search_query=query)

@app.route('/admin/add_book', methods=['POST'])
def add_book_route():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    title = request.form['title']
    author = request.form['author']
    category = request.form['category']
    quantity = int(request.form['quantity'])
    
    # First add the book to get the ID
    add_book(title, author, category, quantity)
    
    # Get the newly added book
    new_book = books_collection.find_one({'title': title, 'author': author})
    
    # Handle file upload
    if 'image_file' in request.files:
        image_file = request.files['image_file']
        if image_file and image_file.filename:
            saved_url = save_image(image_file, str(new_book['_id']))
            if saved_url:
                update_book_image(str(new_book['_id']), saved_url)
                flash(f'Book added successfully with cover image!', 'success')
            else:
                flash('Book added but image upload failed. Please use JPG, PNG, or GIF format.', 'warning')
    else:
        flash('Book added successfully!', 'success')
    return redirect(url_for('admin_dashboard_modern'))

@app.route('/admin/update_book/<book_id>', methods=['POST'])
def update_book_route(book_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    title = request.form['title']
    author = request.form['author']
    category = request.form['category']
    quantity = int(request.form['quantity'])
    
    # Update book details
    update_book(book_id, title, author, category, quantity)
    
    # Handle file upload
    if 'image_file' in request.files:
        image_file = request.files['image_file']
        if image_file and image_file.filename:
            saved_url = save_image(image_file, book_id)
            if saved_url:
                update_book_image(book_id, saved_url)
    
    flash('Book updated successfully!', 'success')
    return redirect(url_for('admin_dashboard_modern'))

@app.route('/admin/delete_book/<book_id>')
def delete_book_route(book_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    delete_book(book_id)
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard_modern'))

@app.route('/admin/delete_user/<user_id>')
def delete_user_route(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    # Prevent admin from deleting themselves
    if user_id == session['user_id']:
        flash('You cannot delete your own account!', 'error')
        return redirect(url_for('admin_dashboard_modern'))
    
    delete_user(user_id)
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard_modern'))

@app.route('/admin/update_book_image/<book_id>', methods=['POST'])
def update_book_image_route(book_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    if 'image_file' in request.files:
        image_file = request.files['image_file']
        if image_file and image_file.filename:
            image_url = save_image(image_file, book_id)
            if image_url:
                update_book_image(book_id, image_url)
                flash('Book image updated successfully!', 'success')
            else:
                flash('Invalid image file. Please upload a valid image.', 'error')
        else:
            flash('No file selected.', 'error')
    else:
        flash('No file in request.', 'error')
    
    return redirect(url_for('admin_dashboard_modern'))

@app.route('/admin/delete_book_image/<book_id>')
def delete_book_image_route(book_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    # Delete the image file
    filename = f"book_{book_id}.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    
    # Update the database to remove image reference
    books_collection.update_one(
        {'_id': ObjectId(book_id)},
        {'$unset': {'image': ''}}
    )
    
    flash('Book image deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard_modern'))

@app.route('/admin/database')
def database_viewer():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    # Get all data from collections
    books_data = list(books_collection.find())
    users_data = list(users_collection.find())
    issued_books_data = list(issued_books_collection.find())
    
    # Convert ObjectIds to strings for display
    for book in books_data:
        book['_id'] = str(book['_id'])
    
    for user in users_data:
        user['_id'] = str(user['_id'])
        # Hide password hashes for security
        if 'password' in user:
            user['password'] = '***HIDDEN***'
    
    for issued in issued_books_data:
        issued['_id'] = str(issued['_id'])
        issued['user_id'] = str(issued['user_id'])
        issued['book_id'] = str(issued['book_id'])
    
    return render_template('database_viewer.html', 
                         books=books_data, 
                         users=users_data, 
                         issued_books=issued_books_data)

@app.route('/user')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        books = get_all_books()
        issued_books = get_issued_books(session['user_id'])
        pending_requests = get_pending_requests(session['user_id'])
        current_user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
        
        # Add wishlist info to each book
        if books:
            for book in books:
                try:
                    book_id_str = str(book['_id'])
                    book['in_wishlist'] = is_in_wishlist(session['user_id'], book_id_str)
                except Exception:
                    book['in_wishlist'] = False
        
        return render_template('student_dashboard_modern.html', books=books, issued_books=issued_books, pending_requests=pending_requests, current_user=current_user)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return redirect(url_for('login'))

@app.route('/user/search', methods=['GET', 'POST'])
def search_books_route():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        query = request.form.get('query', '')
    else:
        query = request.args.get('query', '')
    
    if query:
        books = search_books(query)
    else:
        books = get_all_books()
    
    issued_books = get_issued_books(session['user_id'])
    return render_template('student_dashboard_modern.html', books=books, issued_books=issued_books, search_query=query)

@app.route('/user/issue_book/<book_id>')
def issue_book_route(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if issue_book(session['user_id'], book_id):
        flash('Book issued successfully!', 'success')
    else:
        flash('Book not available', 'error')
    return redirect(url_for('user_dashboard'))

@app.route('/user/request_book/<book_id>')
def request_book_route(book_id):
    """Request a book - creates a pending request"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if create_pending_request(session['user_id'], book_id):
        flash('Book request submitted! Pending admin approval.', 'success')
    else:
        flash('You have already requested this book or it is not available.', 'error')
    return redirect(url_for('user_dashboard'))

@app.route('/admin/issue_book', methods=['POST'])
def admin_issue_book_route():
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    user_id = request.form.get('user_id')
    book_id = request.form.get('book_id')
    if user_id and book_id:
        if issue_book(user_id, book_id):
            flash('Book issued successfully!', 'success')
        else:
            flash('Book not available', 'error')
    else:
        flash('Please select both student and book', 'error')
    return redirect(url_for('admin_dashboard_modern'))

@app.route('/admin/pending_requests')
def admin_pending_requests():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    pending_requests = get_pending_requests()
    books = get_all_books()
    issued_books = get_issued_books()
    users = get_all_users()
    current_user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
    returned_books = len([i for i in issued_books if i.get('return_date')])
    
    return render_template('admin_dashboard_modern.html', 
                         books=books, 
                         issued_books=issued_books, 
                         users=users, 
                         current_user=current_user, 
                         returned_books=returned_books,
                         pending_requests=pending_requests)

@app.route('/admin/approve_request/<request_id>')
def admin_approve_request_route(request_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    if approve_pending_request(request_id):
        flash('Request approved and book issued successfully!', 'success')
    else:
        flash('Failed to approve request. Book may no longer be available.', 'error')
    
    return redirect(url_for('admin_pending_requests'))

@app.route('/admin/reject_request/<request_id>')
def admin_reject_request_route(request_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    reject_pending_request(request_id)
    flash('Request rejected.', 'info')
    
    return redirect(url_for('admin_pending_requests'))

@app.route('/admin/return_book', methods=['POST'])
def admin_return_book_route():
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    user_id = request.form.get('user_id')
    book_id = request.form.get('book_id')
    if user_id and book_id:
        fine = return_book(user_id, book_id)
        if fine is not False:
            if fine == 'already_returned':
                flash('This book has already been returned!', 'info')
            elif fine > 0:
                flash(f'Book returned! Fine: ${fine}', 'warning')
            else:
                flash('Book returned successfully!', 'success')
        else:
            flash('Error returning book', 'error')
    else:
        flash('Please select both student and book', 'error')
    return redirect(url_for('admin_dashboard_modern'))

@app.route('/user/return_book/<book_id>')
def return_book_route(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    fine = return_book(session['user_id'], book_id)
    if fine is not False:
        if fine == 'already_returned':
            flash('This book has already been returned!', 'info')
        elif fine > 0:
            flash(f'Book returned! Fine: ${fine}', 'warning')
        else:
            flash('Book returned successfully!', 'success')
    else:
        flash('Error returning book', 'error')
    return redirect(url_for('user_dashboard'))

@app.route('/user/cancel_request/<book_id>')
def cancel_request_route(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cancel_pending_request(session['user_id'], book_id)
    flash('Request cancelled successfully!', 'success')
    return redirect(url_for('user_dashboard'))

# Wishlist routes
@app.route('/wishlist/add/<book_id>')
def add_to_wishlist_route(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    add_to_wishlist(session['user_id'], book_id)
    flash('Added to wishlist!', 'success')
    
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('user_dashboard'))

@app.route('/wishlist/remove/<book_id>')
def remove_from_wishlist_route(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    remove_from_wishlist(session['user_id'], book_id)
    flash('Removed from wishlist!', 'success')
    
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('user_dashboard'))

# Review routes
@app.route('/book/review/<book_id>', methods=['POST'])
def add_review_route(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment', '')
    
    add_review(book_id, session['user_id'], rating, comment)
    flash('Review added!', 'success')
    
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('user_dashboard'))

# Borrowing history
@app.route('/user/history')
def borrowing_history_route():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    history = get_borrowing_history(session['user_id'])
    current_user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
    
    if session.get('role') == 'admin':
        books = get_all_books()
        issued_books = get_issued_books()
        users = get_all_users()
        return render_template('admin_dashboard.html', books=books, issued_books=issued_books,
                             users=users, current_user=current_user, history=history)
    
    books = get_all_books()
    issued_books = get_issued_books(session['user_id'])
    return render_template('student_dashboard_modern.html', books=books, issued_books=issued_books,
                         current_user=current_user, history=history)

# Returned books - show all returned books available for borrowing
@app.route('/user/returned_books')
def returned_books_route():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get all books that are available (can be borrowed)
    available_books = list(books_collection.find({'available': {'$gt': 0}}))
    
    # Get borrowing history for the current user
    history = get_borrowing_history(session['user_id'])
    current_user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
    
    # Get all issued books for the current user (to show what they currently have)
    issued_books = get_issued_books(session['user_id'])
    
    return render_template('student_dashboard_modern.html', 
                         books=available_books, 
                         issued_books=issued_books,
                         current_user=current_user, 
                         history=history,
                         show_returned=True)

# Library Statistics (Admin only)
@app.route('/admin/stats')
def library_stats_route():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    stats = get_library_stats()
    overdue = get_overdue_books()
    
    books = get_all_books()
    issued_books = get_issued_books()
    users = get_all_users()
    current_user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
    
    return render_template('admin_dashboard.html', books=books, issued_books=issued_books,
                         users=users, current_user=current_user, stats=stats, overdue=overdue)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)