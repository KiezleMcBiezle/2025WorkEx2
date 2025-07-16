from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'securekey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/shopdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)
Session(app)

class User(db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        
        if User.query.filter_by(username=uname).first():
            return "Username already exists. <a href='/register'>Try again</a>"
        
        hashed_pwd = generate_password_hash(pwd)
        new_user = User(username=uname, password=hashed_pwd)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = uname
        return redirect(url_for('products'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        
        user = User.query.filter_by(username=uname).first()
        if user and check_password_hash(user.password, pwd):
            session['user'] = uname
            return redirect(url_for('products'))
        else:
            return "Invalid credentials. <a href='/login'>Try again</a>"

    return render_template('login')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

with app.app_context():
    db.create_all()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    total = db.Column(db.Float)

with app.app_context():
    db.create_all()
    
@app.route('/')
def index():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="shopdb"
    )
    cursor = db.cursor()
    cursor.execute("SELECT product_name,description,image_url FROM products")
    rows = cursor.fetchall()
    products = [{"name":r[0],"description":r[1],"image_url":r[2]} for r in rows]
    db.close()
    username = session.get('username')
    return render_template('products.html', products=products, username=username)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    items = []
    total = 0

    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        subtotal = product.price * qty
        items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
        total += subtotal

    return render_template('cart.html', items=items, total=total)

@app.route('/checkout', methods=['POST'])
def checkout():
    name = request.form['name']
    address = request.form['address']
    cart = session.get('cart', {})
    total = 0

    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        total += product.price * qty

    order = Order(customer_name=name, address=address, total=total)
    db.session.add(order)
    db.session.commit()

    session['cart'] = {}
    return f"<h2>Thanks {name}, your order has been placed!</h2><a href='/'>Back to store</a>"

if __name__ == '__main__':
    app.run(debug=True)
