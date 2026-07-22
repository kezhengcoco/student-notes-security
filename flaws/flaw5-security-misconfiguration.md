# FLAW 5: Security Misconfiguration

## OWASP Top 10 Category

A05:2021 - Security Misconfiguration

## Vulnerable Source

The vulnerable configuration is located at the end of `app.py`.

```python
if __name__ == "__main__":
    app.run(debug=True)
