from flask import Flask, redirect, url_for, session, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    current_user,
    login_required
)
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask-Login configuration
login_manager = LoginManager(app)
login_manager.login_view = 'index'

# User model with a role field ('customer' or 'farmer')
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'customer' or 'farmer'
    # If you're using manual password auth, add a 'password' field here.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Google OAuth configuration (hardcoded credentials)
app.config['GOOGLE_CLIENT_ID'] = "830614235307-479inej7v2ur154b60vts8f354an7fco.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "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"

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

# -------------------------------
# ROUTES
# -------------------------------

@app.route('/')
def index():
    # If the user is logged in, redirect based on their role.
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    # If not logged in, render your integrated login/signup template:
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """
    This function handles manual login when the user
    submits the login form in login.html
    """
    email = request.form.get('email')
    password = request.form.get('password')
    # Example check (assuming you have a password column)
    user = User.query.filter_by(email=email).first()
    if user and password == "your-check-here":
        # For demonstration, just compare plain text
        # In production, use hashing with e.g. check_password_hash
        login_user(user)
        return redirect(url_for('dashboard'))
    else:
        flash("Invalid email or password", "error")
        return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup():
    """
    This function handles manual signup when the user
    submits the signup form in login.html
    """
    name = request.form.get('name')
    email = request.form.get('email')
    role = request.form.get('role')
    password = request.form.get('password')
    # Validate inputs
    if not all([name, email, role, password]):
        flash("Please fill out all fields", "error")
        return redirect(url_for('index'))
    if role not in ['customer', 'farmer']:
        flash("Invalid role selected", "error")
        return redirect(url_for('index'))

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already registered. Please log in.", "error")
        return redirect(url_for('index'))

    # Create new user
    new_user = User(name=name, email=email, role=role)
    # If using password, store hashed version here
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for('dashboard'))

@app.route('/login/google')
def google_login():
    """
    Initiates Google OAuth flow
    """
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/google/callback')
def google_authorize():
    """
    Callback for Google OAuth
    """
    try:
        token = google.authorize_access_token()
        user_info = google.get('userinfo').json()
    except Exception as e:
        flash("Google login failed", "error")
        return redirect(url_for('index'))

    if not user_info or 'email' not in user_info:
        flash("Failed to retrieve user information from Google", "error")
        return redirect(url_for('index'))

    # Check if user already exists
    user = User.query.filter_by(email=user_info['email']).first()
    if user:
        login_user(user)
    else:
        # For new OAuth users, create with default role "customer" (or ask them)
        user = User(
            google_id=user_info['id'],
            name=user_info['name'],
            email=user_info['email'],
            role='customer'
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    """
    Redirect based on user role
    """
    if current_user.role == 'customer':
        return redirect(url_for('home'))
    elif current_user.role == 'farmer':
        return redirect(url_for('farmerhome'))
    else:
        flash("User role is not set correctly", "error")
        return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
    # Home page for customers
    return render_template('home.html', name=current_user.name)

@app.route('/farmerhome')
@login_required
def farmerhome():
    # Home page for farmers
    return render_template('farmerhome.html', name=current_user.name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
