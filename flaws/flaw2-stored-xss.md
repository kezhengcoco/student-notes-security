# FLAW 2: Stored Cross-Site Scripting

## OWASP Top 10 Category

A03:2021 - Injection

## Vulnerable Source

The vulnerable code is located in `templates/notes.html`.

```html
<h2>{{ note["title"] | safe }}</h2>

<p>
    {{ note["content"] | safe }}
</p>
