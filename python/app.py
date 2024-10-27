from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Route for the login page
@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login_post():
    # Retrieve data from form submission
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Simple authentication check (just for demonstration purposes)
    if email == "user@example.com" and password == "password123":
        return redirect(url_for('page2'))
    else:
        return "Login failed. Invalid credentials."

# Route for the second page
@app.route('/page2')
def page2():
    return render_template('page2.html')

if __name__ == '__main__':
    app.run(debug=True)
