import random
import os
from flask import Flask, render_template, request, redirect, session, url_for
from Resources.races import races
from Resources.classes import classes
from Resources.names import names
from Resources.character import character_data

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route("/")
def welcome_page():
    return render_template('welcome.html')


@app.route("/race", methods=['GET', 'POST'])
def race():
    selected_race = None
    if request.method == 'POST':
        selected_race = request.form.get('race')
        with open("Characteristics/race.txt", "w") as file:
            file.write("Race: " + selected_race)
        return redirect('http://127.0.0.1:5000/class')
    return render_template('race.html', races=races, selected=selected_race)


@app.route("/class", methods=['GET', 'POST'])
def class_page():
    selected_class = None
    if request.method == 'POST':
        selected_class = request.form.get('class')
        with open("Characteristics/class.txt", "w") as file:
            file.write('Class: ' + selected_class)
        return redirect('http://127.0.0.1:5000/name')
    return render_template('class.html', classes=classes, selected=selected_class)


@app.route('/name')
def name():
    name = session.get('current_name', '')
    return render_template('name.html', name=name)


@app.route('/generate-name', methods=['GET', 'POST'])
def generate_name():
    name = random.choice(names)
    session['current_name'] = name
    return redirect(url_for('name'))


@app.route('/save-name', methods=['GET', 'POST'])
def save_name():
    current = session.get('current_name', None)
    if current:
        with open("Characteristics/name.txt", "w") as file:
            file.write('Name: ' + current)
        return redirect('http://127.0.0.1:5000/stat-roll')
    return redirect(url_for('name'))


@app.route("/stat-roll")
def stat_roll():
    stats = session.get('current_stats', [])
    return render_template('stat-roll.html', stats=stats)


@app.route('/generate-stats', methods=['GET', 'POST'])
def generate_stats():
    stats = []
    for num in range(6):
        stats.append(random.randint(1, 18))
    session['current_stats'] = stats
    return redirect(url_for('stat_roll'))


@app.route('/save-stats', methods=['GET', 'POST'])
def save_stats():
    current = session.get('current_stats', None)
    if current:
        with open("Characteristics/stats.txt", "w") as file:
            for stat in current:
                file.write(str(stat) + '\n')
        return redirect('http://127.0.0.1:5000/stats')
    return redirect(url_for('stat_roll'))


@app.route("/stats", methods=['GET', 'POST'])
def stats():
    options = [14, 10, 8, 12, 6, 15]
    if request.method == 'POST':
        return redirect('http://127.0.0.1:5000/character')
    return render_template('stats.html', options=options)


@app.route('/character')
def character():
    return render_template('character.html', character=character_data)
