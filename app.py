from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>Student Notes</h1>
    <p>Welcome to the Student Notes application.</p>
    """


if __name__ == "__main__":
    app.run(debug=True)
