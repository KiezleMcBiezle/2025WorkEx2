from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'securekey123'
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)
Session(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # Store hashed password

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if User.query.filter_by(user=uname).first():
            return "Username already exists. <a href='/register'>Try again</a>"
        new_user = User(user=uname, password=pwd)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = uname
        return 
    return 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        user = User.query.filter_by(user=uname, password=pwd).first()
        if user:
            session['user'] = uname
            return redirect(url_for('index'))
        return "Invalid credentials. <a href='/login'>Try again</a>"
    return

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))
