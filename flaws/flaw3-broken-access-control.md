# FLAW 3: Broken Access Control / IDOR

## OWASP Top 10 Category

A01:2021 - Broken Access Control

## Vulnerable Source

The vulnerable code is located in `app.py` in the `/delete-note/<int:note_id>` route.

```python
connection.execute(
    "DELETE FROM notes WHERE id = ?",
    (note_id,)
)
