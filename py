from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "replace_this_with_a_real_secret_key"  # Required for sessions/flash messages

# Temporary in-memory user storage
accounts = {}

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in accounts and accounts[username] == password:
            session["user"] = username
            return f"Welcome, {username}! You are logged in."
        else:
            flash("Invalid username or password.")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/create_account.html", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in accounts:
            flash("Username already exists.")
            return redirect(url_for("create_account"))
        else:
            accounts[username] = password
            flash("Account created successfully!")
            return redirect(url_for("login"))
    return '''
    <form method="POST">
        <label>New Username:</label><br>
        <input type="text" name="username" required><br>
        <label>New Password:</label><br>
        <input type="password" name="password" required><br>
        <button type="submit">Create Account</button>
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
