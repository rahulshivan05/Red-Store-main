from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask.templating import render_template

app = Flask(__name__)
app.debug = True

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
# To suppress warning messages
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Order model


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    # Store cart items as JSON string
    cart_items = db.Column(db.String(500), nullable=False)


# Create the database tables
with app.app_context():
    db.create_all()


@app.route('/2')
def about():
    return render_template('index2.html')


@app.route('/')
def index():
    """Homepage for testing."""
    return """
    <h1>Order Submission API</h1>
    <form action="/submit-order" method="post">
        <label>Name:</label><br>
        <input type="text" name="name"><br><br>
        <label>Email:</label><br>
        <input type="email" name="email"><br><br>
        <label>Address:</label><br>
        <input type="text" name="address"><br><br>
        <label>Phone:</label><br>
        <input type="text" name="phone"><br><br>
        <label>Cart Items (JSON String):</label><br>
        <textarea name="cart_items"></textarea><br><br>
        <button type="submit">Submit Order</button>
    </form>
    """


@app.route('/submit-order', methods=['POST'])
def submit_order():
    """Handle order submission."""
    try:
        # Get form data
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        cart_items = request.form['cart_items']

        # Input validation
        if not all([name, email, address, phone, cart_items]):
            return jsonify({"status": "error", "message": "All fields are required!"}), 400

        # Create a new order instance
        new_order = Order(name=name, email=email, address=address,
                          phone=phone, cart_items=cart_items)

        # Save to database
        db.session.add(new_order)
        db.session.commit()
        return jsonify({"status": "success", "message": "Order received!"}), 201
    except Exception as e:
        print(f"Error: {e}")  # For debugging purposes
        return jsonify({"status": "error", "message": "There was an issue processing your order."}), 500


@app.route('/orders', methods=['GET'])
def get_orders():
    """Retrieve all orders."""
    try:
        orders = Order.query.all()
        result = [
            {
                "id": order.id,
                "name": order.name,
                "email": order.email,
                "address": order.address,
                "phone": order.phone,
                "cart_items": order.cart_items,
            }
            for order in orders
        ]
        return jsonify({"status": "success", "orders": result}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "Could not retrieve orders."}), 500


@app.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Retrieve a specific order by ID."""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"status": "error", "message": "Order not found."}), 404
        result = {
            "id": order.id,
            "name": order.name,
            "email": order.email,
            "address": order.address,
            "phone": order.phone,
            "cart_items": order.cart_items,
        }
        return jsonify({"status": "success", "order": result}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "Could not retrieve the order."}), 500


if __name__ == '__main__':
    app.run()
