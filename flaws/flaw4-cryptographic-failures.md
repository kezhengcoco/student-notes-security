# FLAW 4: Cryptographic Failures

## OWASP Top 10 Category

A04:2021 - Cryptographic Failures

## Vulnerable Source

The vulnerable code is located in `app.py` in the user registration route.

```python
password = request.form["password"]

connection.execute(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    (username, password)
)
