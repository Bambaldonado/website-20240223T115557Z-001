from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

#SqlAlchemy Database Configuration With Mysql
app.config['SECRET_KEY'] = 'Sample secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/pharmacydb'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


#INITIALIZE MODELS
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.Integer)
    role = db.Column(db.String(255))
    created_by = db.Column(db.String(255))
    created_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_by = db.Column(db.String(255))
    updated_date = db.Column(db.DateTime(timezone=True))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    supplier = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    category = db.Column(db.String(255))
    price = db.Column(db.Integer)
    created_by = db.Column(db.String(255))
    created_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_by = db.Column(db.String(255))
    updated_date = db.Column(db.DateTime(timezone=True))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_by = db.Column(db.String(255))
    created_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_by = db.Column(db.String(255))
    updated_date = db.Column(db.DateTime(timezone=True))
#ENDS HERE ---------------------------------------------------------------


#LOGIN QUERY FOR ADMIN
users = {
    'admin': {'password': 'admin', 'role': 'admin'}
}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username]['password'] == password:
        session['username'] = username
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    if users.get(username, {}).get('role') != 'admin':
        return redirect(url_for('login'))

    if request.method == 'GET':
        # Render admin dashboard template
        return render_template('admin_dashboard.html', users=users.values())
    elif request.method == 'POST':
        # Handle form submission or other POST requests
        # (if any)
        pass

@app.route('/admindashboard', methods=['GET', 'POST'])
def admindashboard():
    return render_template('admin_dashboard.html')  
#ENDS HERE ---------------------------------------------------------------

#ROUTING FOR INVENTORY --------------------------------------------------
@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    all_data = Item.query.all()
    return render_template('inventory.html', items = all_data)

@app.route('/insertItem', methods = ['POST'])
def insertItem():

    if request.method == 'POST':

        name = request.form['name']
        supplier = request.form['supplier']
        category = request.form['category']
        quantity = request.form['quantity']
        price = request.form['price']

        new_item = Item(
                    name=name,
                    supplier=supplier,
                    quantity=quantity,
                    category=category,
                    price=price,
        )

        db.session.add(new_item)
        db.session.commit()

        flash("Item Inserted Successfully")

        return redirect(url_for('inventory'))


@app.route('/deleteItem/<id>', methods=['GET', 'POST'])
def deleteItem(id):
    if request.method == 'POST':
        my_data = Item.query.get(id)
        db.session.delete(my_data)
        db.session.commit()
        flash("Item Deleted Successfully")
    return redirect(url_for('inventory'))

    # If the request method is GET (i.e., initial access to the route),
    # you can simply return a redirect response to another page

#ENDS HERE ----------------------------------------------------


#ROUTING FOR SUPPLIER ------------------------------------------
@app.route('/supplier', methods=['GET', 'POST'])
def supplier():
    # Your logic to handle GET and POST requests for the inventory page goes here
    return render_template('supplier.html')

#ROUTING FOR EMPLOYEES ------------------------------------------
@app.route('/employees', methods=['GET', 'POST'])
def employees():
    # Your logic to handle GET and POST requests for the inventory page goes here
    return render_template('employees.html')

#ENDS HERE ----------------------------------------------------




#Automatic creation of tables in the database in mysql
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
