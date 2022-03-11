# save this as app.py
from flask import Flask, escape, request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hbnb')
def hello():
    return 'HBNB'

@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    text = text.replace('_', ' ')
    return f"C {escape(text)}"

@app.route('/python/<text>', strict_slashes=False)
@app.route('/python', strict_slashes=False)
def python_is_cool(text='is_cool'):
    text = text.replace('_', ' ')
    return f"Python {escape(text)}"

@app.route('/number/<int:n>', strict_slashes=False)
def it_is_number(n):
    return f"{escape(n)} is a number"

@app.route('/number_template/<int:n>', strict_slashes=False)
def render(n):
    return render_template('5-number.html', n=n)

@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    return render_template('5-number.html', n=n)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
