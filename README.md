# Student Notes Security Assignment

This project is a simple Flask-based student notes web application created for the Cyber Security Base course project.

The application contains five intentionally introduced security flaws from five different categories of the **OWASP Top 10 2021**. Each flaw is accompanied by a documented fix. The vulnerable code is kept in the application, while the corresponding fixed implementation is provided as commented-out code, as required by the assignment.

The application has a Python Flask backend and uses SQLite as its database.

---

## OWASP Top 10 Version

This project uses the **OWASP Top 10 2021** list.

The five flaws included in the project are:

1. **A01:2021 - Broken Access Control**
2. **A03:2021 - Injection**
3. **A04:2021 - Cryptographic Failures**
4. **A05:2021 - Security Misconfiguration**
5. **A07:2021 - Identification and Authentication Failures**

Each flaw belongs to a different OWASP Top 10 category.

---

## Application Features

The application provides the following functionality:

* User registration
* User login
* User logout
* Creating notes
* Viewing notes
* Deleting notes

The application uses a Flask backend and an SQLite database.

---

## Technologies

* Python
* Flask
* SQLite
* Jinja2
* HTML

---

# Installation and Running Instructions

## 1. Clone the repository

```bash
git clone https://github.com/kezhengcoco/student-notes-security.git
```

Enter the project directory:

```bash
cd student-notes-security
```

---

## 2. Install dependencies

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

The main dependency is Flask.

If the `pip` command is not available, Python's module syntax can be used instead:

```bash
python -m pip install -r requirements.txt
```

---

## 3. Initialize the database

Run:

```bash
python init_db.py
```

This creates the SQLite database and the required tables for users and notes.

---

## 4. Start the application

Run:

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

The application can then be accessed through a web browser.

---

# Security Flaws

## FLAW 1: Broken Access Control / IDOR

### OWASP Category

**A01:2021 - Broken Access Control**

The application allows authenticated users to delete notes by providing a note ID in the URL.

The vulnerable endpoint is:

```text
/delete-note/<note_id>
```

The application checks whether the user is logged in, but does not verify whether the note belongs to the current user.

The vulnerable code is located in the `delete_note` route in `app.py`.

The vulnerable implementation deletes a note using only its ID:

```python
connection.execute(
    "DELETE FROM notes WHERE id = ?",
    (note_id,)
)
```

As a result, an authenticated user may be able to manipulate the note ID and delete another user's note.

The fix is to verify both the note ID and the current user's ID:

```python
connection.execute(
    "DELETE FROM notes WHERE id = ? AND author_id = ?",
    (note_id, session["user_id"])
)
```

The additional ownership check ensures that a user can only delete notes belonging to their own account.

The detailed analysis and fix are documented in:

[FLAW 1 - Broken Access Control](flaws/flaw3-broken-access-control.md)

---

## FLAW 2: SQL Injection

### OWASP Category

**A03:2021 - Injection**

The login functionality constructs an SQL query by directly concatenating user-controlled input.

The vulnerable code is located in the login route in `app.py`.

The vulnerable implementation is:

```python
query = (
    "SELECT * FROM users "
    "WHERE username = '" + username +
    "' AND password = '" + password + "'"
)

user = connection.execute(query).fetchone()
```

Because the username and password are directly inserted into the SQL query, user input can affect the structure of the SQL statement.

This may allow an attacker to manipulate the query and potentially bypass authentication.

The fix is to use parameterized SQL queries:

```python
user = connection.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    (username, password)
).fetchone()
```

With parameterized queries, user input is treated as data rather than executable SQL syntax.

The detailed analysis and fix are documented in:

[FLAW 2 - SQL Injection](flaws/flaw1-sql-injection.md)

---

## FLAW 3: Plaintext Password Storage

### OWASP Category

**A04:2021 - Cryptographic Failures**

The registration functionality stores the original user password directly in the database.

The vulnerable code is located in the registration route in `app.py`:

```python
connection.execute(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    (username, password)
)
```

The password is stored without hashing.

If an attacker obtains access to the database, the original passwords can be read directly. This is particularly dangerous because users may reuse the same password on other services.

The password should instead be processed using a password hashing function before being stored:

```python
from werkzeug.security import generate_password_hash

password_hash = generate_password_hash(password)

connection.execute(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    (username, password_hash)
)
```

During login, the submitted password should be checked against the stored hash using a password verification function such as `check_password_hash`.

The application should never store the original password directly.

The detailed analysis and fix are documented in:

[FLAW 3 - Cryptographic Failures](flaws/flaw4-cryptographic-failures.md)

---

## FLAW 4: Security Misconfiguration

### OWASP Category

**A05:2021 - Security Misconfiguration**

The Flask application is started with debug mode enabled:

```python
app.run(debug=True)
```

Debug mode is useful during development, but it should not be enabled in a production environment.

When an application encounters an error, debug mode may expose detailed information about the application's internal implementation, including error details and other information that could help an attacker.

The fix is to disable debug mode:

```python
app.run(debug=False)
```

A production deployment should also use an appropriate production-grade web server and should avoid exposing detailed internal error information to users.

The detailed analysis and fix are documented in:

[FLAW 4 - Security Misconfiguration](flaws/flaw5-security-misconfiguration.md)

---

## FLAW 5: Weak Password Policy

### OWASP Category

**A07:2021 - Identification and Authentication Failures**

The registration functionality does not enforce a minimum password length or any other password strength requirements.

As a result, users can create accounts using extremely weak passwords such as:

```text
1
123
password
```

Weak passwords are easier to guess using brute-force or dictionary-based attacks.

The vulnerable implementation accepts the password without validating its length or strength.

The fix is to perform server-side password validation before creating the account. For example:

```python
if len(password) < 8:
    return "Password must be at least 8 characters long."
```

The validation must be performed on the backend because client-side validation can be bypassed by directly sending requests to the server.

A stronger implementation could also use additional password requirements and rate limiting.

The detailed analysis and fix are documented in:

[FLAW 5 - Weak Password Policy](flaws/flaw5-weak-password-policy.md)

---

# Screenshots

Screenshots demonstrating the effects of the vulnerabilities before and after applying the fixes are stored in the `screenshots/` directory.

The screenshots follow the naming convention required by the assignment:

```text
flaw-1-before-1.png
flaw-1-after-1.png

flaw-2-before-1.png
flaw-2-after-1.png

flaw-3-before-1.png
flaw-3-after-1.png

flaw-4-before-1.png
flaw-4-after-1.png

flaw-5-before-1.png
flaw-5-after-1.png
```

The screenshots demonstrate the actual effects of each vulnerability and the corresponding behavior after applying the fix.

---

# Educational Purpose

The vulnerabilities in this project are intentionally included for educational purposes as part of the Cyber Security Base course project.

The vulnerable implementations should not be used in production applications.

The purpose of this project is to demonstrate how common web application vulnerabilities can occur in backend code and how they can be mitigated through secure implementation practices.

The project uses the OWASP Top 10 2021 categories and provides both vulnerable implementations and commented-out fixes in the source code.
