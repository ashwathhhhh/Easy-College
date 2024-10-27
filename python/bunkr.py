from bs4 import BeautifulSoup
import requests

loginurl = 'https://ecampus.psgtech.ac.in/studzone2/AttWfLoginPage.aspx'
secure_url = 'https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx'

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
    attendance_table = soup.find('table', {'id': 'PDGcourpercView'})
    
    if attendance_table:
        # Iterate through all rows in the table

        rows = attendance_table.find_all('tr')
        
        # Loop through each row and get cell data

        count = 0
        min_attendance = 75
        min_attendance_exemp = 65
        bunk = 0 
        attend = 0

        for row in rows:
            count= count+1
            #print(count)
            columns = row.find_all('td')
            row_data = [column.get_text(strip=True) for column in columns]  # Extract text from each column
            if count == 1:
                pass
            else:
                html_course_code = ''
                course_code = (row_data[0])
                total_hours = int(row_data[1])
                exemption_hours = int(row_data[2])
                absent_hours = int(row_data[3])
                present_hours = int(row_data[4])
                percentage = int(row_data[5])
                percentage_with_exemption = int(row_data[6])
                percentage_with_med_exemption = int(row_data[7])
               
                # Do something with the data

                total_can_bunk = int(0.25 * float(total_hours))
                total_need_to_attend = int( 0.75 * float(total_hours))
                total_need_to_attend_exemp = int(0.65*total_hours)
                total_can_bunk_exemp = int(0.35 * total_hours)
                if exemption_hours == 0:
                    if percentage >= min_attendance:
                        print('course code =',course_code)
                        bunk = total_can_bunk - absent_hours
                        print('remaining bunk for sem =',bunk)
                    else:
                        attend = total_need_to_attend - present_hours
                        print('attend =',attend)
                else:
                    print("With exemption")
                    if percentage_with_med_exemption >= min_attendance_exemp:
                        print('course code =',course_code)
                        bunk = total_can_bunk_exemp - absent_hours
                        print('remaining bunk for sem =',bunk)

                html_course_code = '23Z311'
                if course_code == html_course_code:
                    if_i_bunk = 4 #replace this 0 with input from HTML file
                    attendance_after_bunk = round(present_hours/(total_hours+if_i_bunk) * 100,2)
                    print('attendance after bunk =',attendance_after_bunk)


                print("\n")
                
    else:
        print("Attendance table not found.")

    


