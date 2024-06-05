from flask import Flask, render_template, request, jsonify
import random
import string

# Initialize the Flask application
app = Flask(__name__)

# Function to generate a random password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))
    

# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data from the request
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Add your signup logic here (e.g., save the user to the database)
        return f"User {username} signed up successfully!"
    # Render the signup page template
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data from the request
        username = request.form['username']
        password = request.form['password']
        # confirm_password = request.form['confirm_password']
        # Add your signup logic here (e.g., save the user to the database)
        return f"User {username} logged in successfully!"
    # Render the signup page template
    return render_template('login.html')

# Route to generate a random password and return it as a JSON response
@app.route('/generate-password')
def generate_password_route():
    # Generate a random password
    password = generate_password()
    # Return the generated password as a JSON response
    return jsonify(password=password)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
