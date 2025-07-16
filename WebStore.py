from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'securekey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/shopdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)
Session(app)

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
    
@app.route('/products')
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
    sort_option = request.args.get("sort", "price_asc")
    type = request.args.get("category")

    query = "SELECT * FROM products"
    filters = []
    params = []

    if type :
        filters.append("type = ?")
        params.append(type)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    if sort_option == "price_asc":
        query += " ORDER BY price ASC"
    elif sort_option == "price_desc":
        query += " ORDER BY price DESC"
    elif sort_option == "name":
        query += " ORDER BY name ASC"
    elif sort_option == "newest":
        query += " ORDER BY id DESC" 

    products = db.execute(query, params).fetchall()
    db.close()
    return render_template("products.html", products=products, type=type, sort=sort_option)

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
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="shopdb"
    )
    name = request.form['name']
    address = request.form['address']
    cart = session.get('cart', {})
    total = 0
    
    cursor = db.cursor()
    cursor.execute("SELECT product_ID,stock FROM products")
    rows = cursor.fetchall()
    products = ({"ID":r[0],"QTY":r[1]} for r in rows)

    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        total += product.price * qty
        if qty > product["QTY"]:
            return "Insufficient Stocks"
        else:
            product.stock -= qty

    order = Order(customer_name=name, address=address, total=total)
    db.session.add(order)
    db.session.commit()

    session['cart'] = {}
    return f"<h2>Thanks {name}, your order has been placed!</h2><a href='/'>Back to store</a>"

if __name__ == '__main__':
    app.run(debug=True)
