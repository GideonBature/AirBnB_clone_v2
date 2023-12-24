#!/usr/bin/python3
"""script that starts a Flask web application
"""
from flask import Flask
from markupsafe import escape

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def index():
    """index page/home page
    Returns: (str) - "Hello HBNB!"
    """
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """sub path
    Returns: (string) - "HBNB"
    """
    return "HBNB"


@app.route('/c/<text>')
def custom_c(text):
    """display C followed by custom text variable
    replaces any underscore(_) symbols with a space( )

    Returns: (string) - C <text>
    """
    for ch in text:
        if ch == '_':
            texts = text.split('_')

            new_text = ''
            for i in range(len(texts)):
                new_text += ' ' + texts[i]

            return f"C{new_text}"

    return f"C {text}"


@app.route('/python')
@app.route('/python/<text>')
def custom_python(text='is cool'):
    """display Python followed by custom text variable
    replaces any underscore(_) symbols with a space( )

    Returns: (string) - Python <text>
    """
    for ch in text:
        if ch == '_':
            texts = text.split('_')

            new_text = ''
            for i in range(len(texts)):
                new_text += ' ' + texts[i]

            return f"Python{new_text}"

    return f"Python {text}"


@app.route('/number/<int:n>')
def number(n):
    """Displays "n is a number" only if n is an integer

    Returns: (string) - "<n> is a number"
    """
    return f"{n} is a number"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
