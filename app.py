from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the SQLite database
def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL)''')
        conn.commit()
        conn.close()

# Function to generate a random password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Safely get form data from the request
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Debugging: Print the form data
        print(f"Received form data: username={username}, password={password}, confirm_password={confirm_password}")
        
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('signup'))

        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            flash('User registered successfully!')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!')
            return redirect(url_for('signup'))
    
    return render_template('index.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Safely get form data from the request
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Debugging: Print the form data
        print(f"Received form data: username={username}, password={password}")
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            flash('User logged in successfully!')
            return redirect(url_for('login'))
        else:
            flash('Invalid username or password!')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Route to generate a random password and return it as a JSON response
@app.route('/generate-password')
def generate_password_route():
    password = generate_password()
    return jsonify(password=password)

# Run the Flask application
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
