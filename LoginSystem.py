import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates')
app.secret_key = "convo_super_secret_key_123"
DB_PATH = "details.db"

# --- DATABASE SETUP ---
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()

# --- HELPER FUNCTIONS ---
def verify_user(username, password):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        row = c.fetchone()
        if row:
            # check_password_hash compares the typed password with the stored hash
            return check_password_hash(row[0], password)
    return False

def add_user(username, password):
    hashed_pw = generate_password_hash(password)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

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
        username = request.form.get("username")
        password = request.form.get("password")

        if verify_user(username, password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        
        # Determine specific error for the UI
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
            user_exists = c.fetchone() is not None

        error = "Incorrect password." if user_exists else "Account not found. Please sign up."

    return render_template("login.html", error=error)

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            error = "Fields cannot be empty."
        elif add_user(username, password):
            # Redirect to the 'login' function after successful creation
            return redirect(url_for("login"))
        else:
            error = "Username already exists."
    
    return render_template("create_account.html", error=error)

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        # Assumes file is at templates/Dashboard/dashboard.html
        return render_template("Dashboard/dashboard.html", username=session["user"])
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# --- ASSETS ROUTE ---
@app.route('/dashboard_assets/<path:filename>')
def serve_dashboard_assets(filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', 'Dashboard'), filename)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
