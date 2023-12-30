#!/usr/bin/python3
"""script that starts a Flask web application
"""
from flask import Flask, render_template
from models import storage


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

    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(exceptions):
    """Remove the current SQLAlchemy Session
    after each request
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
