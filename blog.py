# blog.py - controller
# imports
from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from functools import wraps
from os import path

# configuration
ROOT = path.dirname(path.realpath(__file__))
DATABASE = path.join(ROOT, 'urunner.db')
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'hard_to_guess'


app = Flask(__name__)
# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)


# function used for connecting to the database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first.')
        return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error), status_code


@app.route('/main')
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute('select * from events')
    posts = [dict(title=row[0], post='Date: {} Distance: {}, D+ : {} Time limit: {}'.format(row[1], row[2], row[3], row[4])) for row in cur.fetchall()]
    g.db.close()
    return render_template('main.html', posts=posts)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    event_date = request.form['event date']
    distance = request.form['distance']
    total_climbing = request.form['total climbing']
    time_limit = request.form['time limit']
    itra_points = request.form['itra points']
    utmb_points = request.form['utmb points']
    info = request.form['info']
    event_link = request.form['event link']

    if not title or not event_date or not distance or not total_climbing:
        flash("Fields Title, Event date, Distance and Total climbing are required. Please try again.")
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('insert into events (title, event_date, distance, total_climbing, time_limit, itra_points, utmb_points, info, event_link) values (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     [request.form['title'], request.form['event date'], request.form['distance'], request.form['total climbing'], request.form['time limit'],
                      request.form['itra points'], request.form['utmb points'], request.form['info'], request.form['event link']])
        g.db.commit()
        g.db.close()
        flash('New entry was successfully posted!')
        return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True)
