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
        
        #'txtusercheck': name if name else "",  # Use the username from app.py
        'txtusercheck':"23z360",
        'txtpwdcheck':"04JAN2006",
        #'txtpwdcheck': password if password else "",   # Use the password from app.py
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
        attendance_table = soup.find('table', {'id': 'DgResult'})
        
        if attendance_table:
            # Iterate through all rows in the table

            rows = attendance_table.find_all('tr')

            #define varaiblees
            credits1=0
            count=0
            summation=0
            total_credits=0
            gpa=0
            table = {}
            
            # Loop through each row and get cell data
            for row in rows:
                count+=1
                columns = row.find_all('td')
                row_data = [column.get_text(strip=True) for column in columns] 

                if count==1:
                    pass
                
                else:
                    sem = (row_data[0])
                    course = row_data[1]         
                    title = row_data[2]  
                    credits1 = int(row_data[3])
                    grade = row_data[4]
                    result = row_data[5]
                    print(result)
                    total_credits+=credits1
                    if credits1 ==0:
                        pass
                    elif grade[0:2] == "RA":
                        print("Arrear. No gpa.")
                    else:
                        product= credits1 * int(grade[0:2])
                        summation += product
            
            gpa = summation/total_credits
            print(gpa)
            
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

    
                