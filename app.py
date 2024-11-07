from flask import Flask, redirect, url_for, render_template, request, session
from bunkr import return_data
from Timetable import get_timetable
from calc import get_academic_details

import math

app = Flask(__name__)
app.secret_key = "sh_ashwath_secret_key"  # Replace with a secure secret key

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form["nm"]
        password = request.form["pw"]
        # Store user info in session
        session['user'] = name
        session['logged_in'] = True
        # Store credentials in session
        session['credentials'] = {"name": name, "password": password}
        return redirect(url_for("pages"))
    else:
        # Check if user is already logged in
        if session.get('logged_in'):
            return redirect(url_for("pages"))
        return render_template("login.html")

@app.route("/logout")
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for("login"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/pages", methods=["POST", "GET"])
def pages():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    if request.method == "POST":
        return redirect(url_for("attendance"))
    return render_template("pages.html")

@app.route('/cgpa')
def cgpa():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    academic_data = get_academic_details(session.get('user'), session.get('password'))
    return render_template('cgpa.html', academic_data=academic_data)

@app.route('/attendance')
def attendance():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    
    results = []
    # Get credentials from session
    credentials = session.get('credentials', {})
    rows = return_data(credentials.get("name"), credentials.get("password"))
    timetable = get_timetable(credentials.get("name"), credentials.get("password"))

    if rows is None:
        return "Unable to fetch attendance data. Please check your credentials."
        
    count = 0
    for row in rows:
        count += 1
        columns = row.find_all('td')
        row_data = [column.get_text(strip=True) for column in columns]

        if count == 1:
            pass  # Skip header row 
        else:
            exemption_bunk = 0
            total_present = 0
            threshold = 0.75
            exemption_threshold = 0.65
            
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
                    bunk = math.floor((present_hours-(threshold * total_hours))/threshold)
                    exemption_bunk = 5000
                    results.append({
                        "course_name": course_name,
                        "course_code": course_code,
                        "Physical_Attendance": percentage,
                        "Attendance_Exemption": percentage_with_med_exemption,
                        "status": "Remaining bunks",
                        "bunk": bunk,
                        "exemption_bunks": exemption_bunk
                    })
                else:
                    attend = math.ceil((total_hours - present_hours)/(1-threshold))
                    exemption_bunk = 5000
                    results.append({
                        "course_name": course_name,
                        "course_code": course_code,
                        "Physical_Attendance": percentage,
                        "Attendance_Exemption": percentage_with_med_exemption,
                        "status": "Attend",
                        "bunk": attend,
                        "exemption_bunks": exemption_bunk
                    })
            else:
                if percentage_with_med_exemption >= 75 and percentage >= 65:
                    exemption_present_hours = present_hours + exemption_hours
                    exemption_absent_hours = absent_hours - exemption_hours

                    bunk = math.floor((exemption_present_hours-(threshold * total_hours))/threshold)
                    exemption_bunk = math.floor((present_hours-(exemption_threshold * total_hours))/exemption_threshold)
                    results.append({
                        "course_name": course_name,
                        "course_code": course_code,
                        "Physical_Attendance": percentage,
                        "Attendance_Exemption": percentage_with_med_exemption,
                        "status": "Normal bunks",
                        "bunk": bunk,
                        "exemption_bunks": exemption_bunk,
                        "exemption_hours": exemption_hours,
                        "bunking": exemption_bunk
                    })  
    
    sorted_results = sorted(results, key=lambda x: x['Attendance_Exemption'], reverse=False)
    return render_template('attendance.html', results=sorted_results)

if __name__ == "__main__":
    app.run(debug=True)