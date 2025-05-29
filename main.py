import random
import requests
import os
from flask import Flask, render_template, request, redirect, session, url_for
from Resources.races import races
from Resources.classes import classes
from Resources.names import names

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
            file.write(selected_race)
        return redirect('http://127.0.0.1:5000/class')
    return render_template('race.html', races=races, selected=selected_race)


@app.route("/class", methods=['GET', 'POST'])
def class_page():
    selected_class = None
    if request.method == 'POST':
        selected_class = request.form.get('class')
        with open("Characteristics/class.txt", "w") as file:
            file.write(selected_class)
        return redirect('http://127.0.0.1:5000/name')
    return render_template('class.html', classes=classes, selected=selected_class)


@app.route('/name')
def name():
    name = session.get('current_name', '')
    return render_template('name.html', name=name)


@app.route('/generate-name', methods=['GET', 'POST'])
def generate_name():
    with (open('Characteristics/race.txt', 'r') as char_race, open('Characteristics/class.txt', 'r') as char_class):
        name_request = {
            "race": char_race.read(),
            "class": char_class.read()
        }
    response = requests.post('http://127.0.0.1:5002/gen-name', json=name_request)
    full_name = response.json()

    session['current_name'] = full_name['full_name']
    return redirect(url_for('name'))


@app.route('/save-name', methods=['GET', 'POST'])
def save_name():
    current = session.get('current_name', None)
    if current:
        with open("Characteristics/name.txt", "w") as file:
            file.write(current)
        return redirect('http://127.0.0.1:5000/stat-roll')
    return redirect(url_for('name'))


@app.route("/stat-roll")
def stat_roll():
    stats = session.get('current_stats', [])
    return render_template('stat-roll.html', stats=stats)


@app.route('/generate-stats', methods=['GET', 'POST'])
def generate_stats():
    response = requests.post(f'http://127.0.0.1:5001/roll_stats')
    stats = response.json()
    session['current_stats'] = stats['stat_values']
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
    options = []
    with open("Characteristics/stats.txt", 'r') as file:
        for stat in file:
            options.append(int(stat.strip()))
    return render_template('stats.html', options=options)


@app.route('/submit-stats', methods=['GET', 'POST'])
def submit_stats():
    stats = {
        "STR": request.form.get('str_dropdown'),
        "DEX": request.form.get('dex_dropdown'),
        "CON": request.form.get('con_dropdown'),
        "INT": request.form.get('int_dropdown'),
        "WIS": request.form.get('wis_dropdown'),
        "CHA": request.form.get('cha_dropdown')
    }
    with open('Characteristics/ability-scores.txt', 'w') as file:
        for stat, value in stats.items():
            file.write(f"{stat}:{value}\n")
    return redirect('http://127.0.0.1:5000/character')


@app.route('/character')
def character():
    with (open('Characteristics/race.txt', 'r') as race1, open('Characteristics/class.txt', 'r') as class1,
          open('Characteristics/name.txt', 'r') as name1, open('Characteristics/ability-scores.txt', 'r') as stats1):
        race = race1.read()
        class_ = class1.read()
        name = name1.read()
        stats = {}
        for stat in stats1:
            stat_list = stat.strip().split(':')
            stats[stat_list[0]] = stat_list[1]

    return render_template('character.html', race=race, class_=class_, name=name, stats=stats)
