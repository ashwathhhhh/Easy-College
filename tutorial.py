from flask import Flask, redirect, url_for, render_template, request


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


if __name__ == "__main__":
    app.run(debug=True)