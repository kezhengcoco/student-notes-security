# FLAW 1: SQL Injection

## OWASP Top 10 Category

A03:2021 - Injection

## Vulnerable Source

The vulnerable code is located in `app.py` in the `/login` route.

```python
query = (
    "SELECT * FROM users "
    "WHERE username = '" + username +
    "' AND password = '" + password + "'"
)

user = connection.execute(query).fetchone()
