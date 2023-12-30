#!/usr/bin/python3
"""script that starts a Flask web application
"""
from flask import Flask, render_template
from markupsafe import escape
from models import storage
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/states_list')
def state_list():
    """display a HTML page: inside the tag <BODY>
    <H1> tag: 'States'
    <UL> tag: 'List of all State objects present in DBStorage
    <LI> tag: description of one State
    """
    states = storage.all(State).values()
    states_sorted = sorted(states, key=lambda x: x.name)

    return render_template('7-states_list.html', states=states_sorted)

@app.teardown_appcontext
def teardown_appcontext(exception):
    """Remove the current SQLAlchemy Session
    after each request
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
