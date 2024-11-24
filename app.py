from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
from datetime import datetime, timedelta
from flask_mail import Mail, Message
import os

# Flask app configuration
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USE_TLS'] = True  
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'Your Email Address'
app.config['MAIL_PASSWORD'] = 'Your App Password' 
mail = Mail(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# OTP Model 
class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

# Create tables
with app.app_context():
    db.drop_all()
    db.create_all()

# Fucntion To Send Otp
def send_otp(email):
    otp = ''.join(random.choices(string.digits, k=6))  
    expires_at = datetime.now() + timedelta(minutes=2) 

    # Check if the email already has an OTP entry
    otp_record = OTP.query.filter_by(email=email).first()

    if otp_record:
        # Update the existing record
        otp_record.otp_code = otp
        otp_record.expires_at = expires_at
    else:
        # Create a new record if none exists
        otp_record = OTP(email=email, otp_code=otp, expires_at=expires_at)
        db.session.add(otp_record)

    # Commit the changes to the database
    db.session.commit()

    # Send OTP email
    msg = Message('Your OTP Code', sender='Your Email Address', recipients=[email])
    msg.body = f'Your OTP code is {otp}. It will expire in 2 minutes.'
    mail.send(msg)

# Routes

# Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['email'] = email
            session['logged_in'] = True
            return redirect(url_for('dashboard'))

        flash('Invalid Credentials', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')

# Registration Page with OTP
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['password2']
        
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email is already registered", "error")
            return redirect(url_for('login'))

        # Temporarily save OTP for verification
        send_otp(email)
        session['email'] = email  # Store email in session for OTP verification
        session['username'] = username
        session['password'] = generate_password_hash(password)  # Store hashed password
        flash("OTP sent to your email. Please verify.", "info")
        return redirect(url_for('otpverify'))

    return render_template('register.html')

# OTP Verification Page
@app.route('/otpverify', methods=['GET', 'POST'])
def otpverify():
    if request.method == 'POST':
        otp = request.form['otp']
        email = session.get('email')
        username = session.get('username')
        password = session.get('password')
        
        if not email or not username or not password:
            flash("Session expired or invalid request.", "error")
            return redirect(url_for('register'))

        otp_record = OTP.query.filter_by(email=email).first()
        if not otp_record or otp != otp_record.otp_code or datetime.now() > otp_record.expires_at:
            flash('Invalid or expired OTP', 'error')
            return redirect(url_for('otpverify'))

        # OTP is valid. Register the user.
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Clean up the OTP record
        db.session.delete(otp_record)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('otpverify.html')

# Dashboard Page
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user_email = session.get('email')
    user = User.query.filter_by(email=user_email).first()

    return render_template('dashboard.html', username=user.username)

# Logout Page
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)






