from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

# This secret key is intentionally weak.
# This will later be used as one of the security flaws.
app.secret_key = "secret123"


def get_db_connection():
    connection = sqlite3.connect("notes.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # =========================================
        # FLAW 5: WEAK PASSWORD POLICY
        # OWASP A07:2021 - Identification and
        # Authentication Failures
        # =========================================

        # VULNERABLE VERSION:
        # No minimum password length or password
        # strength validation is implemented.
        #
        # Any password can be accepted, including:
        # "1", "123", or "password".

        # FIXED VERSION:
        
        if len(password) < 8:
             return "Password must be at least 8 characters long."

        connection = get_db_connection()

        try:

            # =========================================
            # FLAW 4: CRYPTOGRAPHIC FAILURES
            # OWASP A04:2021 - Cryptographic Failures
            # =========================================

            # VULNERABLE VERSION:
            # The original password is stored directly
            # in the database without hashing.

            connection.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )

            # FIXED VERSION:
            #
            # from werkzeug.security import generate_password_hash
            #
            # password_hash = generate_password_hash(password)
            #
            # connection.execute(
            #     "INSERT INTO users (username, password) VALUES (?, ?)",
            #     (username, password_hash)
            # )

            connection.commit()

        except sqlite3.IntegrityError:
            connection.close()
            return "Username already exists."

        connection.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_db_connection()

        # ================================
        # FLAW 1: SQL INJECTION
        # OWASP A03: Injection
        # ================================
        
        # VULNERABLE VERSION:
        # User input is directly concatenated into the SQL query.
        # This allows an attacker to manipulate the SQL statement.
        
        query = (
            "SELECT * FROM users "
            "WHERE username = '" + username +
            "' AND password = '" + password + "'"
        )
        
        user = connection.execute(query).fetchone()
        
                
        # FIXED VERSION:
        #
        # from werkzeug.security import check_password_hash
        #
        # user = connection.execute(
        #     "SELECT * FROM users WHERE username = ?",
        #     (username,)
        # ).fetchone()
        #
        # if user and check_password_hash(
        #     user["password"],
        #     password
        # ):
        #     # Login successful

        connection.close()

        if user:

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["is_admin"] = user["is_admin"]

            return redirect("/notes")

        return "Invalid username or password."

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


@app.route("/notes")
def notes():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    notes = connection.execute(
        "SELECT * FROM notes"
    ).fetchall()

    connection.close()

    return render_template(
        "notes.html",
        notes=notes
    )


@app.route("/create-note", methods=["GET", "POST"])
def create_note():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO notes (title, content, author_id)
            VALUES (?, ?, ?)
            """,
            (
                title,
                content,
                session["user_id"]
            )
        )

        connection.commit()
        connection.close()

        return redirect("/notes")

    return render_template("create_note.html")


@app.route("/delete-note/<int:note_id>")
def delete_note(note_id):

    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    # =========================================
    # FLAW 3: BROKEN ACCESS CONTROL / IDOR
    # OWASP A01:2021 - Broken Access Control
    # =========================================

    # VULNERABLE VERSION:
    # The application checks whether the user is logged in,
    # but does not check whether the note belongs to that user.

    connection.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )


    # FIXED VERSION:
    #
    # connection.execute(
    #     "DELETE FROM notes WHERE id = ? AND author_id = ?",
    #     (note_id, session["user_id"])
    # )

    connection.commit()
    connection.close()

    return redirect("/notes")


# =========================================
# FLAW 5: SECURITY MISCONFIGURATION
# OWASP A05:2021 - Security Misconfiguration
# =========================================

# VULNERABLE VERSION:
# Debug mode is enabled.
# Detailed error information may be exposed to users.

if __name__ == "__main__":
    app.run(debug=True)


# FIXED VERSION:
#
# if __name__ == "__main__":
#     app.run(debug=False)
