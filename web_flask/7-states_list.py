# save this as app.py
from flask import Flask, escape, request
from flask import render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.review import Review
import models


app = Flask(__name__)

@app.route('/states_list', strict_slashes=False)
def state_list():
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)

@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    states = storage.all(State)
    if models.storage_t == "db":
        cities = storage.all(City)
    else:
        cities = State.cities()
    return render_template(
                            '7-states_list.html',
                            states=states,
                            cities=cities
                            )

@app.route('/states', strict_slashes=False)
def states():
    states = storage.all(State)
    return render_template(
                            '7-states_list.html',
                            states=states
                            )

@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    states = storage.all(State)
    amenities = storage.all(Amenity)
    if models.storage_t == "db":
        cities = storage.all(City)
    else:
        cities = State.cities()

    return render_template(
                            'index.html',
                            states=states,
                            cities=cities,
                            amenities=amenities
                            )

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    states = storage.all(State)
    amenities = storage.all(Amenity)
    places = storage.all(Place)
    users = storage.all(User)
    if models.storage_t == "db":
        cities = storage.all(City)
    else:
        cities = State.cities()

    return render_template(
                            'index.html',
                            states=states,
                            cities=cities,
                            amenities=amenities,
                            places=places,
                            users=users
                            )


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
