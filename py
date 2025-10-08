import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

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
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if verify_user(username, password):
            session["user"] = username
            return f"✅ Login successful! Welcome, {username}."
        else:
            error = "Incorrect credentials"

    return render_template("login.html", error=error)

@app.route("/create_account.html", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if add_user(username, password):
            return redirect(url_for("login"))
        else:
            return '''
            <html>
            <head>
                <style>
                    body {
                        background-color: #121212;
                        font-family: 'Roboto', sans-serif;
                        color: #ffffff;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }
                    form {
                        background: #292929;
                        padding: 25px;
                        border-radius: 22px;
                        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                        text-align: center;
                        width: 300px;
                    }
                    label {
                        display: block;
                        margin-bottom: 10px;
                        color: #e0e0e0;
                        font-size: 15px;
                        text-align: left;
                    }
                    input[type="text"],
                    input[type="password"] {
                        width: 90%;
                        padding: 10px;
                        margin-bottom: 15px;
                        border: 1px solid #444;
                        border-radius: 14px;
                        background-color: #2a2a2a;
                        color: #ffffff;
                        transition: all 0.3s ease;
                    }
                    input:focus {
                        border: 1px solid #06ebb9;
                        outline: none;
                    }
                    button {
                        width: 100%;
                        padding: 10px;
                        border: none;
                        border-radius: 20px;
                        background-color: #06ebb9;
                        color: #000000;
                        font-size: 16px;
                        cursor: pointer;
                        transition: all 0.4s ease;
                        margin-top: 5px;
                    }
                    button:hover {
                        opacity: 0.6;
                        border: 2px solid #ffffff;
                    }
                    .error {
                        color: #ff6b6b;
                        opacity: 0.7;
                        font-size: 14px;
                        margin-top: 10px;
                    }
                    a {
                        display: block;
                        margin-top: 15px;
                        color: #06ebb9;
                        text-decoration: none;
                        font-size: 14px;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                </style>
            </head>
            <body>
                <form method="POST">
                    <label>New Username:</label>
                    <input type="text" name="username" required><br>
                    <label>New Password:</label>
                    <input type="password" name="password" required><br>
                    <button type="submit">Create Account</button>
                    <div class="error">⚠️ Username already exists. Try another.</div>
                    <a href="/login">Back to Login</a>
                </form>
            </body>
            </html>
            '''

    # Normal (non-error) page
    return '''
    <html>
    <head>
        <style>
            body {
                background-color: #121212;
                font-family: 'Roboto', sans-serif;
                color: #ffffff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            form {
                background: #292929;
                padding: 25px;
                border-radius: 22px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                text-align: center;
                width: 300px;
            }
            label {
                display: block;
                margin-bottom: 10px;
                color: #e0e0e0;
                font-size: 15px;
                text-align: left;
            }
            input[type="text"],
            input[type="password"] {
                width: 90%;
                padding: 10px;
                margin-bottom: 15px;
                border: 1px solid #444;
                border-radius: 14px;
                background-color: #2a2a2a;
                color: #ffffff;
                transition: all 0.3s ease;
            }
            input:focus {
                border: 1px solid #06ebb9;
                outline: none;
            }
            button {
                width: 100%;
                padding: 10px;
                border: none;
                border-radius: 20px;
                background-color: #06ebb9;
                color: #000000;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.4s ease;
                margin-top: 5px;
            }
            button:hover {
                opacity: 0.6;
                border: 2px solid #ffffff;
            }
            a {
                display: block;
                margin-top: 15px;
                color: #06ebb9;
                text-decoration: none;
                font-size: 14px;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <form method="POST">
            <label>New Username:</label>
            <input type="text" name="username" required><br>
            <label>New Password:</label>
            <input type="password" name="password" required><br>
            <button type="submit">Create Account</button>
            <a href="/login">Back to Login</a>
        </form>
    </body>
    </html>
    '''


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
