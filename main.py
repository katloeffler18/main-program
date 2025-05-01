import random

from flask import Flask, render_template, request, redirect
from Resources.races import races
from Resources.classes import classes
from Resources.names import names

app = Flask(__name__)


@app.route("/")
def welcome_page():
    return render_template('welcome.html')


@app.route("/race", methods=['GET', 'POST'])
def race():
    selected_race = None
    if request.method == 'POST':
        selected_race = request.form.get('race')
        print(selected_race)
        return redirect('http://127.0.0.1:5000/class')
    return render_template('race.html', races=races, selected=selected_race)


@app.route("/class", methods=['GET', 'POST'])
def class_page():
    selected_class = None
    if request.method == 'POST':
        selected_class = request.form.get('class')
        print(selected_class)
        return redirect('http://127.0.0.1:5000/name')
    return render_template('class.html', classes=classes, selected=selected_class)


@app.route("/name")
def name():
    name_flag = request.args.get('generateName')
    if name_flag:
        return render_template('name.html', name=names[random.randint(0, 2)])
    return render_template('name.html')

