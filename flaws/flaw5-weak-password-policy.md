# FLAW 5: Weak Password Policy

## OWASP Top 10 Category

A07:2021 - Identification and Authentication Failures

## Vulnerable Source

The vulnerable code is located in the registration functionality in `app.py`.

The application accepts the password submitted by the user without checking its length or strength.

```python
username = request.form["username"]
password = request.form["password"]
