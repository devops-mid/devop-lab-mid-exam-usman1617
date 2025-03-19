from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User
import re

def is_valid_email(email):
    """Validate email format (case-insensitive)"""
    return re.match(r"^[^@]+@[^@]+\.[^@]+$", email, re.IGNORECASE)

def is_valid_phone(phone):
    """Ensure phone is numeric and exactly 10 digits"""
    return re.match(r"^\d{10}$", phone)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name'].strip()
    email = request.form['email'].strip().lower()  # Normalize email to lowercase
    phone = request.form.get('phone', '').strip()

    # Validate input
    if not name:
        flash("Name field cannot be empty!", "error")
        return redirect(url_for('index'))

    if not is_valid_email(email):
        flash("Invalid email format! Please enter a valid email.", "error")
        return redirect(url_for('index'))

    if phone and not is_valid_phone(phone):
        flash("Phone number must be exactly 10 digits!", "error")
        return redirect(url_for('index'))

    # Check for existing email in the database
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already exists! Try a different one.", "error")
        return redirect(url_for('index'))

    try:
        # Add new user to database
        user = User(name=name, email=email, phone=phone)
        db.session.add(user)
        db.session.commit()
        flash("User added successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while adding the user. Please try again.", "error")

    return redirect(url_for('index'))

