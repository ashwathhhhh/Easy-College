from bs4 import BeautifulSoup
import requests

def return_data(name=None, password=None):
    loginurl = 'https://ecampus.psgtech.ac.in/studzone2/AttWfLoginPage.aspx'
    secure_url = 'https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx'

    # Scrape the VIEWSTATE and EVENTVALIDATION
    viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
    eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']


    # Payload for logging in
    payload = {
        '__VIEWSTATE': viewstate,
        '__EVENTVALIDATION': eventvalidation,
        'rdolst':'S',
        
        'txtusercheck': name if name else "",  # Use the username from app.py
        
        'txtpwdcheck': password if password else "",   # Use the password from app.py
        'abcd3':'Login'
    }

    try:
        with requests.session() as s:
            # Post the login data to the login URL
            login_response = s.post(loginurl, data=payload)
            
            # Access the secure URL after login
            r = s.get(secure_url)
            soup = BeautifulSoup(r.content, 'html.parser')

            # Find the table by its ID
            attendance_table = soup.find('table', {'id': 'PDGcourpercView'})
            
            if attendance_table:
                # Get all rows from the table
                rows = attendance_table.find_all('tr')
                return rows
            else:
                return None

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None
