from bs4 import BeautifulSoup
import requests

loginurl = 'https://ecampus.psgtech.ac.in/studzone2/AttWfLoginPage.aspx'
secure_url = 'https://ecampus.psgtech.ac.in/studzone2/FrmEpsStudResult.aspx'

# Payload for logging in
payload = {
    '__VIEWSTATE':'wfjaEYy0FI1sC/VPcVi24QcJ31uKgMtfa3AcGJvkFG5eYcjfXGwp6jMbiyeOYHyuetWIJaXF3LgTGOWxWGk7HHwSXcbCWViqfnYAteJFkelInRUDFPrCs7G7yLAQ1GpX2js6Ki7c6HXZbkQTvYkIZkxxNG//Sxq0BFgFlqs0PyvLnVXQoBvwSFgztVKjrBhS7P6PyBMb9dQj88s3wTN9TvwlH1v5wm9euE12PWvSN4A=',
    '__VIEWSTATEGENERATOR':'E64D2FFE',
    '__EVENTVALIDATION':'g5OBX22lxevnco1RsfI7lUiyxoHI+6VULprfgdME6INMMlo9Oe0BE9gsycWj2DoX8swZzfek9Gr8MUiNflq8lcySikpulwQQKUI94CndKh0SPQllSuWIBvtwz4v5zyv7t0nmgGBQbO/ig3RUhsl2m4c5NCz/SW5+pDQ586mCeUKc3/jmmcX+BqQ2XCyalh6g7zlwC2SDlptxBPOGGd5wIuc9wmXmLC9FwvRXYNRe3JHHjcSiZtJchiYIEhCnlcG4iOMjPH6I47HS9TRKX8co2Sy7KCa5s1Fdk3zVjSIZjL8=',
    'rdolst':'S',
    'txtusercheck':'23z309',
    'txtpwdcheck':'ashwath',
    'abcd3':'Login'
}

with requests.session() as s:
    # Post the login data to the login URL
    s.post(loginurl, data=payload)
    
    # Access the secure URL after login
    r = s.get(secure_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find the table by its ID
    attendance_table = soup.find('table', {'id': 'DgResult'})
    
    if attendance_table:
        # Iterate through all rows in the table

        rows = attendance_table.find_all('tr')
        
        # Loop through each row and get cell data
        for row in rows:
            count= count+1
            #print(count)
            columns = row.find_all('td')
            row_data = [column.get_text(strip=True) for column in columns]  # Extract text from each column
            print(row_data)