from flask import Flask, redirect, url_for, render_template, request
from bunkr import return_data

app = Flask(__name__)

@app.route("/", methods = ["POST","GET"])
def login():
    if request.method == "POST":
        name = request.form["nm"]
        password = request.form["pw"]
        print(name,password,sep = "\n")
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
    rows = return_data()
    # Process the rows
    count = 0
    for row in rows:
        count += 1
        columns = row.find_all('td')
        row_data = [column.get_text(strip=True) for column in columns]  # Extract text from each column

        if count == 1:
            pass  # Skip header row
        else:
            print(row_data)
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

            if exemption_hours == 0:
                if percentage >= 75:
                    bunk = total_can_bunk - absent_hours
                    results.append({
                        "course_code": course_code,
                        "status": "Remaining bunks for semester",
                        "value": bunk
                    })
                else:
                    attend = total_need_to_attend - present_hours
                    results.append({
                        "course_code": course_code,
                        "status": "Need to attend more classes",
                        "value": attend
                    })
            else:
                if percentage_with_med_exemption >= 65:
                    bunk = total_can_bunk_exemp - absent_hours
                    results.append({
                        "course_code": course_code,
                        "status": "Remaining bunks with exemption",
                        "value": bunk
                    })

    # Pass results to the template
    return render_template('attendance.html', results=results)
    
    


if __name__ == "__main__":
    app.run(debug=True)