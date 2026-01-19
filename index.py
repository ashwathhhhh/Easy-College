from flask import Flask, redirect, url_for, render_template, request, session, send_from_directory, jsonify
from bunkr import return_data as bunkr_return_data
from calc import return_data as calc_return_data
from Timetable import get_timetable
from name import return_data as name_return_data
from cgpa_calculator import return_data as cgpa_calculator_return_data
import math

app = Flask(__name__)
app.secret_key = "sh_ashwath_secret_key"  # Replace with a secure secret key

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            name = data.get("nm")
            password = data.get("pw")
        else:
            name = request.form["nm"]
            password = request.form["pw"]

        session['username'] = name
        session['credentials'] = {"name": name, "password": password}
        
        authenticated = name_return_data(session.get('credentials', {}).get("name"), session.get('credentials', {}).get("password"))
        
        if authenticated is None:
            session['logged_in'] = False
            if request.is_json:
                return jsonify({"success": False, "error": "Incorrect Password or Username"})
            else:
                return render_template("login.html", error="Incorrect Password")
        else:
            session['logged_in'] = True
            if request.is_json:
                return jsonify({"success": True, "redirect_url": url_for("pages")})
            else:
                return redirect(url_for("pages"))
    else: # GET
        if session.get('logged_in'):
            return redirect(url_for("pages"))
        return render_template("login.html")

@app.route('/static/<path:filename>')
def assets(filename):
    return send_from_directory('static', filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

@app.route("/logout")
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for("login"))

@app.route("/about")
def about():
    username = session.get('username', 'User  ')
    return render_template("about.html", username=username)

@app.route("/pages")
def pages():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    
    username = session.get('username', 'User  ')
    name = name_return_data(session.get('credentials', {}).get("name"), session.get('credentials', {}).get("password"))
    return render_template("pages.html", name=name, username=username)

@app.route("/feedback")
def feedback():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    
    return redirect("https://feedbackauto.streamlit.app/")

@app.route('/cgpa')
def cgpa():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    
    username = session.get('username', 'User  ')
    credits1 = 0
    count = 0
    summation = 0
    total_credits = 0
    gpa = 0    
    table = []
    global gpa_result
    gpa_result = None
    l = [0]
    a = 0
    

    credentials = session.get('credentials', {})
    rows2 = calc_return_data(credentials.get("name"), credentials.get("password"))

    if rows2 is None:
        return render_template("cgpa_notavail.html")
    abc = rows2

    for row111 in abc:
        count += 1
        columns11 = row111.find_all('td')
        row_data111 = [column.get_text(strip=True) for column in columns11]
        #print(row_data1)
        for i in row_data111:
            if i.isnumeric():
                l.append(int(i))
                break
            elif i == '':
                break
        m = max(l)
    count = 0
    for row1 in rows2:
        count += 1
        columns = row1.find_all('td')
        row_data1 = [column.get_text(strip=True) for column in columns]
        if count == 1:
            pass
        else:        
            sem = (row_data1[0])
            course = row_data1[1]         
            title = row_data1[2]  
            credits1 = int(row_data1[3])
            grade = row_data1[4]
            result = row_data1[5]                        
            
            if sem == str(m):
                a = a +1
            if sem == str(m) or sem == '':
                if a != 0:

                    table.append({
                        "sem": sem,
                        "course": course,
                        "title": title,
                        "grade": grade,
                        "credits": credits1,
                    })
                    total_credits += credits1
                    if credits1 == 0:
                        pass
                    elif grade[0:2] == "RA" or grade[0:2] == "0 ":
                        gpa_result = 0
                    else:
                        product = credits1 * int(grade[0:2])
                        summation += product
                

    if gpa_result != 0:
        gpa = summation/total_credits    
        gpa = round(gpa, 2)
        return render_template('cgpa.html', table=table, gpa=gpa, total_credits=total_credits, username=username)
    else:
        return render_template('cgpa.html', table=table, gpa='NO CGPA', total_credits=total_credits, username=username)

@app.route('/attendance')
def attendance():   
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    
    username = session.get('username', 'User  ')
    results = []
    # Get credentials from session
    credentials = session.get('credentials', {})
    rows = bunkr_return_data(credentials.get("name"), credentials.get("password"))
    timetable = get_timetable(credentials.get("name"), credentials.get("password"))

    if rows is None:
        return render_template("attendance_update.html")
        
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
            updated_till = row_data[9]

            total_can_bunk = int(0.25 * float(total_hours))
            total_need_to_attend = int(0.75 * float(total_hours))
            total_need_to_attend_exemp = int(0.65 * total_hours)
            total_can_bunk_exemp = int(0.35 * total_hours)
            course_name = timetable[course_code]
            
            if percentage == percentage_with_med_exemption:
                if percentage >= 75:
                    bunk = math.floor((present_hours-(threshold * total_hours))/threshold)
                    if bunk < 0:
                        bunk = 0
                    
                    results.append({
                        "course_name": course_name,
                        "course_code": course_code,
                        "total_hours": total_hours,
                        "present_hours": present_hours,
                        "Physical_Attendance": percentage,
                        "Attendance_Exemption": percentage_with_med_exemption,
                        "updated_till": updated_till,
                        "status": "Remaining bunks",
                        "bunk": bunk,
                        "exemption_bunks": exemption_bunk
                    })
                else:
                    attend = math.ceil((threshold * total_hours - present_hours)/(1-threshold))
                    results.append({
                        "course_name": course_name,
                        "course_code": course_code,
                        "total_hours": total_hours,
                        "present_hours": present_hours,
                        "Physical_Attendance": percentage,
                        "Attendance_Exemption": percentage_with_med_exemption,
                        "updated_till": updated_till,
                        "status": "Attend",
                        "bunk": attend,
                        "exemption_bunks": exemption_bunk
                    })
            else:
                if percentage_with_med_exemption >= 75 and percentage >= 65:
                    bunk = max(0, math.floor((present_hours - (threshold * total_hours)) / threshold))
                    exemption_bunk = 0
                    medical_exemptions = math.floor((percentage_with_med_exemption*total_hours)/100 - exemption_hours)
                    medical_exemptions = medical_exemptions - present_hours
                    exemption_hours = medical_exemptions + exemption_hours
                    percentage1 = percentage
                    percentage2 = percentage_with_med_exemption
                    dexemption_bunk = exemption_bunk
                    while percentage1 > 65 and percentage2 > 75:
                        dexemption_bunk+=1
                        percentage1 = math.ceil(present_hours/(total_hours + dexemption_bunk)*100)
                        percentage2 = math.ceil((present_hours + exemption_hours)/(total_hours + dexemption_bunk)*100)
                        if percentage1 > 65 and percentage2 > 75:
                            exemption_bunk += 1
                            
                    results.append({
                        "course_name": course_name,
                        "course_code": course_code,
                        "total_hours": total_hours,
                        "present_hours": present_hours,
                        "Physical_Attendance": percentage,
                        "Attendance_Exemption": percentage_with_med_exemption,
                        "updated_till": updated_till,
                        "status": "Normal bunks",
                        "bunk": bunk,
                        "exemption_bunks": exemption_bunk,
                        "exemption_hours": exemption_hours,
                        "bunking": exemption_bunk
                    })  
                else:
                    medical_exemptions = math.floor((percentage_with_med_exemption*total_hours)/100 - exemption_hours)
                    medical_exemptions = medical_exemptions - present_hours
                    exemption_hours = medical_exemptions + exemption_hours
                    if percentage_with_med_exemption<75 and percentage > 65:
                        attend = math.ceil(((threshold * total_hours) - (present_hours+exemption_hours))/(1-threshold))
                        results.append({    
                            "course_name": course_name,
                            "course_code": course_code,
                            "total_hours": total_hours,
                            "present_hours": present_hours,
                            "Physical_Attendance": percentage,
                            "Attendance_Exemption": percentage_with_med_exemption,
                            "updated_till": updated_till,
                            "status": "Attend",
                            "bunk": attend,
                            "result.bunk_or_attend" : "attend"
                        })
                    else:
                        attend=math.ceil(((exemption_threshold * total_hours) - present_hours)/(exemption_threshold))
                        results.append({    
                            "course_name": course_name,
                            "course_code": course_code,
                            "total_hours": total_hours,
                            "present_hours": present_hours,
                            "Physical_Attendance": percentage,
                            "Attendance_Exemption": percentage_with_med_exemption,
                            "updated_till": updated_till,
                            "status": "Attend",
                            "bunk": attend,
                            "result.bunk_or_attend" : "attend"
                        })


    
    sorted_results = sorted(results, key=lambda x: x['Attendance_Exemption'], reverse=False)
    return render_template('attendance.html', results=sorted_results, username=username)

@app.route("/loading")
def loading():
    username = session.get('username', 'User  ')
    return render_template("loading.html", username=username)

@app.route('/cgpa_calculator')
def cgpa_calculator():   
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    
    username = session.get('username', 'User')
    credentials = session.get('credentials', {})
    rows = cgpa_calculator_return_data(credentials.get("name"), credentials.get("password"))

    grades = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5}
    
    total_credit_points = 0
    total_credits = 0
    sem_data = {}

    count = 0
    for row in rows:
        count += 1
        columns = row.find_all('td')
        row_data = [column.get_text(strip=True) for column in columns]
        
        if count in (1, 2, len(rows)-1, len(rows)):
            continue

        # 🔹 Skip course code 23Z010 (field index 1)
        if row_data[1].lower() in ["23z010", "23n010"]:
            continue
        
        if row_data[7] == "RA":
            return render_template('cgpa_not_avail.html', username=username)

        if int(row_data[7]) != 0 and row_data[3] != "OEL":
            grade = row_data[6]
            credits = int(row_data[7])
            grade_points = grades.get(grade, 0)
            sem = int(row_data[4])

            total_credits += credits
            total_credit_points += grade_points * credits
            sem_data.setdefault(sem, []).append((grade_points, credits))

    sgpa_cgpa_semwise = []
    cumulative_credits = 0
    cumulative_cp = 0

    for sem in sorted(sem_data.keys()):
        sem_cp_total = sum(gp * cr for gp, cr in sem_data[sem])
        sem_credits = sum(cr for _, cr in sem_data[sem])
        sgpa = round(sem_cp_total / sem_credits, 2) if sem_credits else 0

        cumulative_cp += sem_cp_total
        cumulative_credits += sem_credits
        cgpa_till_now = round(cumulative_cp / cumulative_credits, 2) if cumulative_credits else 0

        sgpa_cgpa_semwise.append({
            'sem': sem,
            'sgpa': sgpa,
            'cgpa': cgpa_till_now
        })

    result = {
        'total_credits': total_credits,
        'credit_points_total': total_credit_points,
        'cgpa': round(total_credit_points / total_credits, 2) if total_credits > 0 else 0
    }

    return render_template(
        'real_cgpa.html',
        result=result,
        semwise_data=sgpa_cgpa_semwise,
        username=username
    )
if __name__ == '__main__':
    app.run(debug=True)