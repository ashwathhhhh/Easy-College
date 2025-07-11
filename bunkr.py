from bs4 import BeautifulSoup
import requests

def return_data(name=None, password=None):
    loginurl = 'https://ecampus.psgtech.ac.in/studzone2/AttWfLoginPage.aspx'
    secure_url = 'https://ecampus.psgtech.ac.in/studzone2/AttWfpercview.aspx'

    # Scrape the VIEWSTATE and EVENTVALIDATION
    #viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
    #eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']


    # Payload for logging in
    payload = {
        '__VIEWSTATE':'wfjaEYy0FI1sC/VPcVi24QcJ31uKgMtfa3AcGJvkFG5eYcjfXGwp6jMbiyeOYHyuetWIJaXF3LgTGOWxWGk7HHwSXcbCWViqfnYAteJFkelInRUDFPrCs7G7yLAQ1GpX2js6Ki7c6HXZbkQTvYkIZkxxNG//Sxq0BFgFlqs0PyvLnVXQoBvwSFgztVKjrBhS7P6PyBMb9dQj88s3wTN9TvwlH1v5wm9euE12PWvSN4A=',
        '__VIEWSTATEGENERATOR':'E64D2FFE',
        '__EVENTVALIDATION':'g5OBX22lxevnco1RsfI7lUiyxoHI+6VULprfgdME6INMMlo9Oe0BE9gsycWj2DoX8swZzfek9Gr8MUiNflq8lcySikpulwQQKUI94CndKh0SPQllSuWIBvtwz4v5zyv7t0nmgGBQbO/ig3RUhsl2m4c5NCz/SW5+pDQ586mCeUKc3/jmmcX+BqQ2XCyalh6g7zlwC2SDlptxBPOGGd5wIuc9wmXmLC9FwvRXYNRe3JHHjcSiZtJchiYIEhCnlcG4iOMjPH6I47HS9TRKX8co2Sy7KCa5s1Fdk3zVjSIZjL8=',
        'rdolst':'S',
        
        'txtusercheck': name if name else "",  # Use the username from app.py
        
        'txtpwdcheck': password if password else "",   # Use the password from app.py
        'abcd3':'Login'
    }

    

    if name == '23z310':
        payload={
            '__VIEWSTATE':'8c8AqwAmVym81aUrDp8RFx3oXfdhTNN7A05rnCq6xS5fwT2FdRp+23oMR6LtkYGCAbYEfG6wFoCqQo8zJhQeM4lMF/Yg0hQMx6+BFT/wWKU43FjwpnkWLl7vUjo1QI4pI2lrxWYaUvaOvSl66rmMuLrj1qiA176KZsGyOo3s6LJSUzXUmbeZDGwZtUqrwYAscgJspFTztwl/DhImaF2dZVMomivkXcMtA61T4nmkyZmMKsYXMi65di+JV6TCU1ELVEoEG+q/cNT55xftLgb5OCGgVtdzgOgpp/A61D3PZpaOzhPbNrtG5YZszuG2gyum',
        '__VIEWSTATEGENERATOR':'E64D2FFE',
        '__EVENTVALIDATION':'9ag7nfwJsCEQ4vbAZGdxIxZys5DdYSChp6dQx4EVAH5800CHJ3WajMxLFiugVucqMgA17RnWMPhm6N/pNH2mY9Z/HwnHJ0MMZVZzpNv7B0j0b49+X8+OzzjJAX+4QawP4DQcMFA7DG5JY00giYG2O6+crNIQc1JYld1TB8wrGZspkW6ZBvucgZrXAMzASm0aO3qUNveJZCOPwB7n6OoKKIwx1UyfepRa0JZwNG9Yen5nHW+Pnqcoyki7N+ZgS7NTpf7mSiJFLzwbPy9yU3Zjq2L2VU4/UGrrdFYm4ACn0Ns=',
        'rdolst':'P',
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
