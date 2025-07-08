
A full-stack web application built with Flask that simulates an online marketplace. Users can create accounts (restricted to @colorado.edu emails), log in securely, and add listings with title, price, and description. The app includes user authentication with password hashing and SQLite database integration.

## Features

- User registration with email validation and secure password hashing  
- Login/logout functionality with session management (basic placeholder)  
- Add, view, and list marketplace items with user association  
- SQLite database for data persistence via SQLAlchemy ORM  
- Flask-Migrate for database migrations  
- Responsive UI with HTML templates (Jinja2)

## Technologies

- Python 3  
- Flask  
- Flask-SQLAlchemy  
- Flask-Migrate  
- Werkzeug Security (password hashing)  
- SQLite

## Setup

1. Clone the repo  
2. Create and activate a virtual environment  
3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
Initialize the database:

bash
Copy
Edit
flask db init  
flask db migrate  
flask db upgrade
Run the app:

bash
Copy
Edit
flask run
Open your browser at http://127.0.0.1:5000

Notes
User authentication is basic and assumes a placeholder logged-in user for adding listings. A full session management system would be needed for production.

Email registration is restricted to @colorado.edu domains to simulate institutional access control.

Future Improvements
Implement full user session management and logout

Add listing edit/delete functionality

Improve UI/UX design and responsiveness

Deploy to a cloud platform for public access
