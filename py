import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
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

# --- ADD USER ---
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

# --- CHECK LOGIN ---
def verify_user(username, password):
    conn = sqlite3.connect("details.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# --- ROUTES ---
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if verify_user(username, password):
            session["user"] = username
            return f"✅ Login successful! Welcome, {username}."
        else:
            flash("❌ Invalid username or password.")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/create_account.html", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if add_user(username, password):
            flash("✅ Account created successfully!")
            return redirect(url_for("login"))
        else:
            flash("⚠️ Username already exists. Try another.")
            return redirect(url_for("create_account"))

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
    init_db()  # ensure the DB + table exists
    app.run(debug=True)
