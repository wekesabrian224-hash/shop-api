from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite///duka.db'
db= SQLAchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock,
        }

    def __repr__(self):
        return f'<Product {self.id}: {self.name}>'

products = [
    {'id': 1, 'name': 'Headphones', 'price': 2500, 'stock': 10},
    {'id': 2, 'name': 'Phone case', 'price': 600, 'stock': 40},
]

def find_product(product_id):
    for product in products:
        if product['id'] == product_id:
            return product
    return None

def validate_product(data, partial=False):
    if not isinstance(data, dict):
        return 'Send a JSON object as the body'

    if 'name' in data or not partial:
        name = data.get('name')
        if not isinstance(name, str) or not name.strip():
            return 'name is required'

    if 'price' in data or not partial:
        price = data.get('price')
        if not isinstance(price, int) or price <= 0:
            return 'price must be a positive whole number'

    if 'stock' in data:
        stock = data['stock']
        if not isinstance(stock, int) or stock < 0:
            return 'stock must be 0 or more'

    return None

@app.get('/')
def home():
    return {'message': 'Welcome to Duka API'}


@app.get('/about')
def about():
    return {'name': 'Lucky', 'message': 'Learning backend at Moringa'}
    
@app.get('/api/health')
def health():
    return jsonify({'status': 'ok'}), 200

@app.get('/api/products')
def list_products():
    return jsonify(products), 200


@app.get('/api/products/<int:product_id>')
def get_product(product_id):
    product = find_product(product_id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product), 200

@app.post('/api/products')
def create_product():
    global next_id
    data = request.get_json(silent=True)

    problem = validate_product(data)
    if problem:
        return jsonify({'error': problem}), 400

    product = {
        'id': next_id,
        'name': data['name'].strip(),
        'price': data['price'],
        'stock': data.get('stock', 0),
    }
    next_id += 1
    products.append(product)
    return jsonify(product), 201


@app.patch('/api/products/<int:product_id>')
def update_product(product_id):
    product = find_product(product_id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json(silent=True)
    problem = validate_product(data, partial=True)
    if problem:
        return jsonify({'error': problem}), 400

    if 'name' in data:
        product['name'] = data['name'].strip()
    if 'price' in data:
        product['price'] = data['price']
    if 'stock' in data:
        product['stock'] = data['stock']
    return jsonify(product), 200



@app.delete('/api/products/<int:product_id>')
def delete_product(product_id):
    product = find_product(product_id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    products.remove(product)
    return '', 204    


@app.errorhandler(404)  #are funvtions that flask runs when a articular error is met 
def not_found(error):
    return jsonify({'error': 'Route not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405    