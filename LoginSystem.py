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

        # check if username exists (for distinct message)
        conn = sqlite3.connect("details.db")
        c = conn.cursor()
        c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        user_exists = c.fetchone() is not None
        conn.close()

        if verify_user(username, password):
            session["user"] = username
            return f"✅ Login successful! Welcome, {username}."
        elif not user_exists:
            error = "Create an account"
        else:
            error = "Incorrect credentials"

    return render_template("Login.html", error=error)

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
            font-family: 'Roboto', sans-serif;
            background-color: rgb(3, 3, 3);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            color: #ffffff;
            flex-direction: column; // BEGIN:
        }
        form {
            background: rgba(31, 31, 31, 0.9);
            padding: 30px;
            border-radius: 25px;
            border: 3px solid #272727;
            width: 400px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }
        
        h2 {
            text-align: center;
            margin-bottom: 20px;
        }

        h1 {
            text-align: center; // END:
            margin-bottom: 700px;
            color: #06ebb9;
        }

        label {
            display: block;
            margin-bottom: 10px;
            color: #e0e0e0;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            margin-right: 10px;
            border: 2px solid #353535;
            border-radius: 25px;
            background-color: #222222;
            color: #ffffff;
            transition: border-color 0.3s;
        }

        input:focus {
                        border: 2px solid #555555;
                        outline: none;
                    }
        button {
            width: 100%;
            padding: 10px;
            border: 2px solid #44444467;
            border-radius: 20px;
            background-color: #222222;
            color: #ffffff;
            border: 2px solid #353535;
            margin-top: 10px;
        }
        button[type="button"] {
            background-color: #999999;
        }
        button:hover {
            background-color: #373737;
            box-shadow: 0 4px 30px #373737a0;
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
                        color: #ffffff;
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
                background-color: rgb(3, 3, 3);
                font-family: 'Roboto', sans-serif;
                color: #ffffff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            form {
                background: rgba(31, 31, 31, 0.9);
                padding: 30px;
                border-radius: 25px;
                border: 3px solid #272727;
                width: 400px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            
            h1 {
                text-align: center;
                margin-bottom: 20px;
                color: #ffffff;
            }

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
                width: 100%;
                padding: 10px;
                margin-bottom: 15px;
                border: 2px solid #353535;
                border-radius: 14px;
                background-color: #2a2a2a;
                color: #ffffff;
                transition: all 0.3s ease;
            }
            input:focus {
                border: 2px solid #555555;
                outline: none;
            }
            button {
                width: 100%;
                padding: 12px;
                border: none;
                border-radius: 25px;
                background-color: #5625c9;
                color: #ffffff;
                font-size: 16px;
                cursor: pointer;
                margin-top: 50px;
                margin-bottom: 10px;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #6a3cd4;
                box-shadow: 0 4px 30px #6a3cd4a0;);
            }
            a {
                text-align: center;
                display: block;
                margin-top: 15px;
                color: #ffffff;
                text-decoration: none;
                font-size: 14px;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Create Account</h1>
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
