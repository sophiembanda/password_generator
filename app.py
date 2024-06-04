from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Add your signup logic here (e.g., save the user to the database)
        return f"User {username} signed up successfully!"
    return render_template('index.html')

@app.route('/generate-password')
def generate_password_route():
    password = generate_password()
    return jsonify(password=password)

if __name__ == '__main__':
    app.run(debug=True)
