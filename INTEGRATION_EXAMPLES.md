# Integration Examples for Glassmorphism Components

## 1. Using the Glassmorphism Login Page

### Option A: Replace Existing Login (Recommended)

Edit your `app.py`:

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_type = request.form.get('login_type', 'student')
        
        user = find_user(username)
        if user and verify_password(user, password):
            user_role = user.get('role', 'student')
            
            if login_type == 'admin' and user_role != 'admin':
                flash('Please use Admin Login', 'error')
                return render_template('glassmorphism_login.html')
            elif login_type == 'student' and user_role == 'admin':
                flash('Please use Admin Login', 'error')
                return render_template('glassmorphism_login.html')
            
            session['user_id'] = str(user['_id'])
            session['role'] = user_role
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('glassmorphism_login.html')  # Use new template
```

### Option B: Keep Existing, Add New Route

```python
@app.route('/login-glass', methods=['GET', 'POST'])
def login_glass():
    # Same logic as login()
    return render_template('glassmorphism_login.html')
```

---

## 2. Using Admin Dashboard Background

### Update `templates/admin_dashboard.html`

Replace this:
```html
<!-- Video Background -->
<div class="video-background">
    <video autoplay muted loop playsinline id="bg-video">
        <source src="https://assets.mixkit.co/videos/..." type="video/mp4">
    </video>
    <div class="video-overlay"></div>
</div>
```

With this:
```html
<!-- Glassmorphism Background -->
<div class="dashboard-background">
    <img src="{{ url_for('static', filename='uploads/admin_dashboard_bg.png') }}" 
         alt="Dashboard Background"
         loading="lazy">
</div>
```

### Add CSS

Add to your existing CSS file or create `static/css/admin_glassmorphism.css`:

```css
.dashboard-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    z-index: -2;
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.dashboard-background img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

/* Ensure content appears above background */
.admin-dashboard {
    position: relative;
    z-index: 1;
}

/* Make dashboard widgets stand out */
.dashboard-card,
.widget {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
}
```

---

## 3. Customizing Colors

### Edit `static/css/glassmorphism_style.css`

```css
:root {
    /* Change to your brand colors */
    --primary-color: #YOUR_HEX_COLOR;
    --secondary-color: #YOUR_SECONDARY_COLOR;
    
    /* Glass effect tweaks */
    --glass-bg: rgba(255, 255, 255, 0.15);  /* Increase for more opaque */
    --glass-border: rgba(255, 255, 255, 0.25);
    --backdrop-blur: blur(20px);  /* Increase/decrease blur */
}
```

### Example: Purple Theme

```css
:root {
    --primary-color: #9333ea;        /* Purple */
    --secondary-color: #7c3aed;      /* Dark purple */
    --success-color: #a78bfa;        /* Light purple */
}
```

### Example: Green Theme

```css
:root {
    --primary-color: #047857;        /* Dark green */
    --secondary-color: #059669;      /* Medium green */
    --success-color: #10b981;        /* Light green */
}
```

---

## 4. Adding to Flask Templates

### Update `templates/base.html`

Add the glassmorphism CSS:

```html
<!DOCTYPE html>
<html>
<head>
    <!-- Existing CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    
    <!-- Add glassmorphism CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/glassmorphism_style.css') }}">
    
    {% block style %}{% endblock %}
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

---

## 5. Creating More Glassmorphism Elements

### Glass Button

```html
<button class="btn btn-primary">
    <span class="btn-text">Click Me</span>
    <span class="btn-icon">→</span>
</button>

<style>
    button.btn {
        /* Inherits from glassmorphism_style.css */
    }
</style>
```

### Glass Card

```html
<div class="glass-card">
    <h3>Your Content</h3>
    <p>Beautiful glass effect</p>
</div>

<style>
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
</style>
```

### Glass Input

```html
<input type="text" class="form-input" placeholder="Type something...">

<style>
    .form-input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        color: white;
        padding: 12px 16px;
        border-radius: 8px;
    }
    
    .form-input:focus {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(99, 102, 241, 0.5);
    }
</style>
```

---

## 6. Responsive Design

The glassmorphism CSS is already responsive, but here's how to customize:

```css
/* Desktop */
@media (min-width: 1024px) {
    .auth-card {
        max-width: 480px;
    }
}

/* Tablet */
@media (max-width: 768px) {
    .auth-card {
        max-width: 90%;
        padding: 1rem;
    }
}

/* Mobile */
@media (max-width: 480px) {
    .auth-card {
        max-width: 100%;
        padding: 0.75rem;
    }
}
```

---

## 7. Video Background Fallback

If video doesn't play, add fallback:

```html
<video class="video-background" autoplay muted loop>
    <source src="{{ url_for('static', filename='uploads/login_background.mp4') }}" type="video/mp4">
    <!-- Fallback image if video doesn't load -->
    <img src="{{ url_for('static', filename='uploads/admin_dashboard_bg.png') }}" 
         alt="Background"
         style="width: 100%; height: 100%; object-fit: cover;">
</video>
```

---

## 8. Adding Animations

### Slide In Animation

```css
@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.auth-card {
    animation: slideInUp 0.6s ease-out;
}
```

### Fade & Scale

```css
@keyframes fadeScale {
    from {
        opacity: 0;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

.btn {
    animation: fadeScale 0.3s ease-out;
}
```

### Hover Glow

```css
.btn-primary:hover {
    box-shadow: 
        0 6px 25px rgba(99, 102, 241, 0.6),
        0 0 30px rgba(139, 92, 246, 0.3);
    transform: translateY(-2px);
}
```

---

## 9. JavaScript Integration

### Password Strength Indicator

```javascript
const passwordInput = document.getElementById('signup_password');
const strengthBar = document.querySelector('.strength-bar');

passwordInput.addEventListener('input', function() {
    const strength = calculatePasswordStrength(this.value);
    updateStrengthBar(strength);
});

function calculatePasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z\d]/.test(password)) strength++;
    return strength;
}

function updateStrengthBar(strength) {
    const colors = ['#ff4757', '#ff9f43', '#ffa502', '#26de81', '#20bf6b'];
    const widths = ['20%', '40%', '60%', '80%', '100%'];
    
    strengthBar.style.width = widths[strength - 1] || '0';
    strengthBar.style.backgroundColor = colors[strength - 1] || '#ccc';
}
```

### Form Toggle

```javascript
function showSignUp() {
    document.getElementById('loginCard').classList.add('hidden');
    document.getElementById('signupCard').classList.remove('hidden');
}

function showLogin() {
    document.getElementById('signupCard').classList.add('hidden');
    document.getElementById('loginCard').classList.remove('hidden');
}
```

---

## 10. Complete Example - Flask Route with Setup

```python
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        login_type = request.form.get('login_type', 'student')
        
        # Your authentication logic here
        user = authenticate_user(username, password)
        
        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('glassmorphism_login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    return render_template('admin_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
```

---

## ✨ Summary

You now have:
- ✅ Glasmorphism login page
- ✅ Admin dashboard background
- ✅ Reusable CSS components
- ✅ All customization options
- ✅ Integration examples

**Start using them in your project!**

