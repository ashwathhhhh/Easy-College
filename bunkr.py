from bs4 import BeautifulSoup
import requests

def return_data(name=None, password=None):
    loginurl = 'https://ecampus.psgtech.ac.in/studzone2/AttWfLoginPage.aspx'
    secure_url = 'https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx'

    # Payload for logging in
    payload = {
        '__VIEWSTATE':'wfjaEYy0FI1sC/VPcVi24QcJ31uKgMtfa3AcGJvkFG5eYcjfXGwp6jMbiyeOYHyuetWIJaXF3LgTGOWxWGk7HHwSXcbCWViqfnYAteJFkelInRUDFPrCs7G7yLAQ1GpX2js6Ki7c6HXZbkQTvYkIZkxxNG//Sxq0BFgFlqs0PyvLnVXQoBvwSFgztVKjrBhS7P6PyBMb9dQj88s3wTN9TvwlH1v5wm9euE12PWvSN4A=',
        '__VIEWSTATEGENERATOR':'E64D2FFE',
        '__EVENTVALIDATION':'g5OBX22lxevnco1RsfI7lUiyxoHI+6VULprfgdME6INMMlo9Oe0BE9gsycWj2DoX8swZzfek9Gr8MUiNflq8lcySikpulwQQKUI94CndKh0SPQllSuWIBvtwz4v5zyv7t0nmgGBQbO/ig3RUhsl2m4c5NCz/SW5+pDQ586mCeUKc3/jmmcX+BqQ2XCyalh6g7zlwC2SDlptxBPOGGd5wIuc9wmXmLC9FwvRXYNRe3JHHjcSiZtJchiYIEhCnlcG4iOMjPH6I47HS9TRKX8co2Sy7KCa5s1Fdk3zVjSIZjL8=',
        'rdolst':'S',
        #'txtusercheck': '23z362',
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
