from flask import render_template, g
import sqlite3
from contextlib import closing
from app import app

app.config.from_object('config')

def connect_db():
    return sqlite3.connect(DATABASE)


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Cookr')


@app.route('/view_foods')
def view_foods():
    cur = g.db.execute('SELECT name, "group" FROM food ORDER BY name')
    entries = [dict(name=row[0], group=row[1]) for row in cur.fetchall()]
    return render_template('view_foods.html', title="Cookr", entries=entries)


@app.route('/view_recipes')
def view_recipes():
    cur = g.db.execute('''SELECT name, description, instructions
                          FROM recipe
                          ORDER BY id''')
    entries = [dict(name=row[0], description=row[1],
               instructions=row[2]) for row in cur.fetchall()]
    return render_template('view_recipes.html', title="Cookr", entries=entries)

'''
@app.route('/add_food', methods=['POST'])
def add_food():
    g.db.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/add_recipes', methods=['POST'])
def add_recipe():
    g.db.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))'''
