from bs4 import BeautifulSoup

# Open the HTML file
with open('logun.html', 'r') as f:
    html_content = f.read()

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Find the input fields for username and password
username_input = soup.find('input', {'name': 'username'})
password_input = soup.find('input', {'name': 'password'})

# Extract the values (if any)
username = username_input.get('value') if username_input else None
password = password_input.get('value') if password_input else None

print("Username:", username)
print("Password:", password)