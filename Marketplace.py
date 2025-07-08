from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='temmy')  # Adjust this if your templates folder has a custom name

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Listing Model
class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    user = db.relationship('User', backref=db.backref('listings', lazy=True))

# Function to generate a list of example listings (now replaced by database queries)
def generate_listings():
    return Listing.query.all()

# Route for the homepage
@app.route('/')
def home():
    listings = generate_listings()  # Fetch all listings from the database
    return render_template('index.html', listings=listings)

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return redirect(url_for('home'))
        else:
            return jsonify({'error': 'Invalid login credentials'}), 400

    listings = generate_listings()
    return render_template('login.html', listings=listings)

# Route for the create account page
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate email domain
        if not email.endswith('@colorado.edu'):
            return jsonify({'error': 'Only @colorado.edu emails are allowed'}), 400

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Account with this email already exists'}), 400

        # Create a new user
        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': 'Account created successfully'}), 201

    listings = generate_listings()
    return render_template('create_account.html', listings=listings)

# Route for adding a new listing
@app.route('/add_listing', methods=['GET', 'POST'])
def add_listing():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        description = request.form.get('description')
        user_id = 1  # For now, assume user ID 1 is logged in (you need a session system for real authentication)

        new_listing = Listing(title=title, price=price, description=description, user_id=user_id)
        db.session.add(new_listing)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add_listing.html')

if __name__ == "__main__":
    app.run(debug=True)
