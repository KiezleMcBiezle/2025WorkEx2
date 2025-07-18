from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
=======
from flask_session import Session
import mysql.connector
>>>>>>> 6c4d6ab25275dee5ae60a73c7db61563aefaffac
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secretkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/shopdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

<<<<<<< HEAD
# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
=======
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
>>>>>>> 6c4d6ab25275dee5ae60a73c7db61563aefaffac

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    colour = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.Column(db.Text, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully. Please log in.')
        return redirect(url_for('login'))
    return render_template('Register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            session['user_id'] = user.id
            session['cart'] = []
            return redirect(url_for('store'))
        flash('Invalid username or password.')
    return render_template('Login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
<<<<<<< HEAD
def about():
    return render_template('About.html')

# Store & Cart routes
@app.route('/store')
def store():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Get query parameters
    product_type = request.args.get('type')
    colour = request.args.get('colour')
    sort_by = request.args.get('sort_by')  # e.g. 'price_asc', 'price_desc', 'name_asc', etc.

    # Start building the query
    query = Product.query

    if product_type:
        query = query.filter_by(type=product_type)
    if colour:
        query = query.filter_by(colour=colour)

    # Sorting logic
    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'name_asc':
        query = query.order_by(Product.name.asc())
    elif sort_by == 'name_desc':
        query = query.order_by(Product.name.desc())

    products = query.all()

    return render_template('Store.html', products=products)
=======
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
>>>>>>> 6c4d6ab25275dee5ae60a73c7db61563aefaffac

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cart_items = []
    total = 0
    if 'cart' in session:
        for item_id in session['cart']:
            product = Product.query.get(item_id)
            if product:
                cart_items.append(product)
                total += product.price
    return render_template('Cart.html', cart_items=cart_items, total=total,int=int )

@app.route('/checkout')
def checkout():
    if 'user_id' not in session or 'cart' not in session:
        return redirect(url_for('login'))

    cart_items = session['cart']
    total = 0
    for item_id in cart_items:
        product = Product.query.get(item_id)
        if product:
            total += product.price

    order = Order(
        user_id=session['user_id'],
        items=",".join(map(str, cart_items)),
        total_price=total
    )
    db.session.add(order)
    db.session.commit()

    session['cart'] = []
    flash('Order placed successfully.')
    return redirect(url_for('store'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        try:
            session['cart'].remove(product_id)
            session.modified = True
        except ValueError:
            pass
    return redirect(url_for('cart'))

@app.route('/orders')
def orders():
    query = Product.query
    if 'user_id' not in session:
        return redirect(url_for('login'))
    orders = Order.query.filter_by(user_id=session['user_id']).all()
    Products = {str(product.id): product for product in Product.query.all()}

    return render_template('Orders.html', orders=orders, Products=Products,int=int)

if __name__ == "__main__":
    app.run(debug=True)
