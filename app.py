# -*- coding: utf-8 -*-
import os
import sys

import click
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)




@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    name = 'Grey Li'

    user = User(name=name)
    # res = 0    
    db.session.add(user)
    # db.session.add(res)

    db.session.commit()
    click.echo('Done.')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


# class Movie(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(60))
#     year = db.Column(db.String(4))


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        x = int(request.form['group'])
        y = int(request.form['group1'])

        if not x > 0 or not y >0:
            flash('Invalid input.')
            return redirect(url_for('index'))
        res = x*y
        # return redirect(url_for('index'))
        return render_template('index.html',res = res)

    # movies = Movie.query.all()
    return render_template('index.html')
