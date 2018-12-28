#!/usr/bin/env python
# -*- coding:utf-8 -*
# @Author   : Zhxu
# @Time     : 18-12-27 下午9:40

# imports
import os

from flask import Flask, request, session, g, redirect, url_for,\
    abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy


# get the folder where this file runs
basedir = os.path.abspath(os.path.dirname(__file__))


# configuration
DATABASE = 'flaskx.db'
DEBUG = True
SECRET_KEY = 'my_precious'
USERNAME = 'admin'
PASSWORD = 'admin'

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# database config
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False

# create and initialize app
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

import models

# @app.route('/')
# def hello():
#     return 'Hello, World!'

# @app.route('/')
# def index():
#     """Searches the database for entries, then displays them."""
#     db = get_db()
#     cur = db.execute('select * from entries order by id desc')
#     entries = cur.fetchall()
#     return render_template('index.html', entries=entries)


@app.route('/')
def index():
    """Searches the database for entries, then displays them."""
    entries = db.session.query(models.Flaskx)
    return render_template('index.html', entries=entries)







"""
Essentially, we want to open a database connection, 
create the database based on the schema if it doesn't already exist, 
then close the connection each time a test is ran.
"""
#
#
# # connect to database
# def connect_db():
#     """Connects to the database."""
#     rv = sqlite3.connect(app.config['DATABASE'])
#     rv.row_factory = sqlite3.Row
#     return rv
#
#
# # create the database
# def init_db():
#     with app.app_context():
#         db = get_db()
#         with app.open_resource('schema.sql', mode='r') as f:
#             db.cursor().executescript(f.read())
#         db.commit()
#
#
# # open database connection
# def get_db():
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db
#
#
# # close database connection
# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()


# @app.route('/add', methods=['POST'])
# def add_entry():
#     """Add new post to database."""
#     if not session.get('logged_in'):
#         abort(401)
#     db = get_db()
#     db.execute(
#         'insert into entries (title, text) values (?, ?)',
#         [request.form['title'], request.form['text']]
#     )
#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_entry():
    """Adds new post to the database."""
    if not session.get('logged_in'):
        abort(401)
    new_entry = models.Flaskx(request.form['title'], request.form['text'])
    db.session.add(new_entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login/authentication/session management."""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """User logout/authentication/session management."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


# @app.route('/delete/<post_id>', methods=['GET'])
# def delete_entry(post_id):
#     """Delete post from database"""
#     result = {'status': 0, 'message': 'Error'}
#     try:
#         db = get_db()
#         db.execute('delete from entries where id=' + post_id)
#         db.commit()
#         result = {'status': 1, 'message': "Post Deleted"}
#     except Exception as e:
#         result = {'status': 0, 'message': repr(e)}
#
#     return jsonify(result)


@app.route('/delete/<int:post_id>', methods=['GET'])
def delete_entry(post_id):
    """Deletes post from database."""
    result = {'status': 0, 'message': 'Error'}
    try:
        new_id = post_id
        db.session.query(models.Flaskr).filter_by(post_id=new_id).delete()
        db.session.commit()
        result = {'status': 1, 'message': "Post Deleted"}
        flash('The entry was deleted.')
    except Exception as e:
        result = {'status': 0, 'message': repr(e)}
    return jsonify(result)


@app.route('/search/', methods=['GET'])
def search():
    query = request.args.get("query")
    entries = db.session.query(models.Flaskx)
    if query:
        return render_template('search.html', entries=entries, query=query)
    return render_template('search.html')


if __name__ == '__main__':
    # init_db()
    app.run()
