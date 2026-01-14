import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory

# We set the template folder to 'templates' explicitly
app = Flask(__name__, template_folder='templates')
app.secret_key = "replace_this_with_a_real_secret_key"

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("details.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# --- HELPER FUNCTIONS ---
def verify_user(username, password):
    conn = sqlite3.connect("details.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def add_user(username, password):
    conn = sqlite3.connect("details.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        result = True
    except sqlite3.IntegrityError:
        result = False
    conn.close()
    return result

# --- ROUTES ---

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if verify_user(username, password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        
        # Check if user exists just for the error message
        conn = sqlite3.connect("details.db")
        c = conn.cursor()
        c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        user_exists = c.fetchone() is not None
        conn.close()

        if not user_exists:
            error = "Create an account"
        else:
            error = "Incorrect credentials"

    # Note: Assuming you have a Login.html in templates/Login.html
    # If Login.html is also in Dashboard, change to "Dashboard/Login.html"
    return render_template("Login.html", error=error)

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        # POINTING TO: templates/Dashboard/dashboard.html
        return render_template("Dashboard/dashboard.html", username=session["user"])
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if add_user(username, password):
            return redirect(url_for("login"))
        return "Username already exists <a href='/create_account'>Try again</a>"
    
    # Simple HTML for creation
    return '''
    <form method="post">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Create Account</button>
    </form>
    '''

# --- SPECIAL ROUTE FOR JS ---
# This allows Flask to serve script.js from the templates/Dashboard folder
@app.route('/dashboard_assets/<path:filename>')
def serve_dashboard_assets(filename):
    # This points to templates/Dashboard
    return send_from_directory(os.path.join(app.root_path, 'templates', 'Dashboard'), filename)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
