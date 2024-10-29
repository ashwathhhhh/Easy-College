from bs4 import BeautifulSoup
import requests

loginurl = 'https://ecampus.psgtech.ac.in/studzone2/AttWfLoginPage.aspx'
secure_url = 'https://ecampus.psgtech.ac.in/studzone2/CAMarks_View.aspx'

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
    attendance_table = soup.find('table', {'id': '8^1600'})
    marks_table = soup.find('table', {'id': '8^1740'})
    marks2_table = soup.find('table', {'id': '8^2210'})
    marks3_table = soup.find('table', {'id': '8^2220'})
    
    if attendance_table:
        # Iterate through all rows in the table

        rows = attendance_table.find_all('tr')
        
        # Loop through each row and get cell data

        count = 0

        for row in rows:
            count= count+1
            columns = row.find_all('td')
            row_data = [column.get_text(strip=True) for column in columns] 
            #print(row_data) # Extract text from each column
            if count == 1 or count == 2:
                pass
            else:
                course_code = row_data[0]
                total_internal = row_data[6]
                if total_internal:

                    print("Course code:",course_code,"Total:",total_internal)
                else:
                    print("Course code:",course_code,"Total: Not Updated Yet")
    
    if marks_table:
        # Iterate through all rows in the table

        rows1 = marks_table.find_all('tr')
        
        # Loop through each row and get cell data

        count1 = 0

        for row1 in rows1:
            count1= count1+1
            columns1 = row1.find_all('td')
            row_data1 = [column1.get_text(strip=True) for column1 in columns1] 
            #print(row_data1) # Extract text from each column
            if count1 == 1 or count1 == 2:
                pass
            else:
                course_code1 = row_data1[0]
                total_internal1 = row_data1[2]
                if total_internal1 != "*":

                    print("Course code:",course_code1,"Total:",total_internal1)
                else:
                    print("Course code:",course_code1,"Total: Not Updated Yet")
    
    if marks2_table:
        # Iterate through all rows in the table

        rows3 = marks2_table.find_all('tr')
        
        # Loop through each row and get cell data

        count3= 0

        for row3 in rows3:
            count3= count3+1
            columns3 = row3.find_all('td')
            row_data3 = [column3.get_text(strip=True) for column3 in columns3] 
            #print(row_data) # Extract text from each column
            if count3 == 1 or count3 == 2:
                pass
            else:
                course_code3 = row_data3[0]
                total_internal3 = row_data3[9]
                if total_internal3:

                    print("Course code:",course_code3,"Total:",total_internal3)
                else:
                    print("Course code:",course_code3,"Total: Not Updated Yet")
    
if marks3_table:
        # Iterate through all rows in the table

        rows4 = marks3_table.find_all('tr')
        
        # Loop through each row and get cell data

        count4 = 0

        for row4 in rows4:
            count4= count4+1
            columns4 = row4.find_all('td')
            row_data4 = [column4.get_text(strip=True) for column4 in columns4] 
            #print(row_data) # Extract text from each column
            if count4 == 1 or count4 == 2:
                pass
            else:
                course_code4= row_data4[0]
                total_internal4 = row_data4[9]  
                if total_internal4 != "*":

                    print("Course code:",course_code4,"Total:",total_internal4)
                else:
                    print("Course code:",course_code4,"Total: Not Updated Yet")

        
            

    


