from app import app
from flask import render_template, url_for

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/login')
def login():
    return render_template('login.html', title='Auth')

@app.route('/register')
def register():
    return render_template('register.html', title='Reg')