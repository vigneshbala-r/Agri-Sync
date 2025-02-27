from flask import Flask, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = "dev-secret"

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Google OAuth Config (Hardcoded Credentials)
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

# Routes
@app.route('/')
def home():
    if current_user.is_authenticated:
        return f"Welcome {current_user.name}! <a href='/logout'>Logout</a>"
    return "Home Page - <a href='/login'>Login with Google</a>"

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/google/callback')
def authorize():
    try:
        token = google.authorize_access_token()
        if not token:
            flash("Login failed. Please try again.", "danger")
            return redirect(url_for('home'))
        
        user_info = google.get('userinfo').json()
        
        # Check if user exists
        user = User.query.filter_by(google_id=user_info['id']).first()

        if not user:
            # Create new user
            user = User(
                google_id=user_info['id'],
                name=user_info['name'],
                email=user_info['email']
            )
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash("Login successful!", "success")
        return redirect(url_for('home'))
    
    except Exception as e:
        flash(f"Authorization failed: {str(e)}", "danger")
        return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You have logged out.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
