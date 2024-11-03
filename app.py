from flask import Flask, redirect, url_for, render_template, request
from bunkr import return_data
from Timetable import timetable

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form["nm"]
        password = request.form["pw"]
        # Store credentials in session or pass them to return_data function
        global credentials
        credentials = {"name": name, "password": password}
        return redirect(url_for("pages"))
    else:
        return render_template("login.html")

@app.route("/pages",methods = ["POST","GET"])
def pages():
    if request.method == "POST":
        return redirect(url_for("attendance"))
    else:
        return render_template("pages.html")

@app.route('/attendance')
def attendance():
    results = []
    # Pass the credentials to return_data function
    rows = return_data(credentials["name"], credentials["password"])
    
    if rows is None:
        return "Unable to fetch attendance data. Please check your credentials."
        
    # Rest of your attendance processing code remains the same
    count = 0
    for row in rows:
        # ... (rest of your existing code)
        count += 1
        columns = row.find_all('td')
        row_data = [column.get_text(strip=True) for column in columns]  # Extract text from each column

        if count == 1:
            pass  # Skip header row 
        else:
            exemption_bunk=0
            total_present=0
            
            course_code = row_data[0]
            total_hours = int(row_data[1])
            exemption_hours = int(row_data[2])
            absent_hours = int(row_data[3])
            present_hours = int(row_data[4])
            percentage = int(row_data[5])
            percentage_with_exemption = int(row_data[6])
            percentage_with_med_exemption = int(row_data[7])

            total_can_bunk = int(0.25 * float(total_hours))
            

            total_need_to_attend = int(0.75 * float(total_hours))
            total_need_to_attend_exemp = int(0.65 * total_hours)
            total_can_bunk_exemp = int(0.35 * total_hours)
            course_name = timetable[course_code]
            if exemption_hours == 0:
                if percentage >= 75:
                    bunk = total_can_bunk - absent_hours
                    dummy = bunk//4
                    bunk += dummy
                    print(course_name)
                    print("bunk:",bunk)
                    print("dummy:", dummy)
                    results.append({
                        "course_name": course_name,
                        "course_code": course_code,
                        "Physical_Attendance" : percentage,
                        "Attendance_Exemption" : percentage_with_med_exemption,
                        "status": "Remaining bunks",
                        "value": bunk
                    })
                else:
                    attend = total_need_to_attend - present_hours
                    results.append({
                        "course_name": course_name,
                        "course_code": course_code,
                        "Physical_Attendance" : percentage,
                        "Attendance_Exemption" : percentage_with_med_exemption,
                        "status": "Attend",
                        "value": attend
                    })
            else:
                if percentage_with_med_exemption >= 75 and percentage >= 65:
                    
                    medical_absent = absent_hours - exemption_hours
                    medical_bunk = total_can_bunk - medical_absent
                    bunk_using_exemption = abs(medical_bunk - (total_can_bunk_exemp - absent_hours))    
                    print()
                    
                    results.append({
                        "course_name": course_name,
                        "course_code": course_code,
                        "Physical_Attendance" : percentage,
                        "Attendance_Exemption" : percentage_with_med_exemption,
                        "status": "Remaining bunks",
                        "value": bunk
                    })  
    sorted_results = sorted(results, key=lambda x: x['Attendance_Exemption'], reverse=False)

    # Pass results to the template
    return render_template('attendance.html', results=sorted_results)

if __name__ == "__main__":
    app.run(debug=True) 