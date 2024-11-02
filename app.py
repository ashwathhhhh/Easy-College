from flask import Flask, redirect, url_for, render_template, request
from bunkr import get_attendance_data

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

@app.route("/pages")
def pages():
    return render_template("pages.html")

@app.route('/attendance')
def attendance():
    attendance_data = get_attendance_data()
    return render_template('attendance.html', **attendance_data)


if __name__ == "__main__":
    app.run(debug=True)