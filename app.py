from flask import Flask, request, jsonify
app = Flask(__name__)

products = [
    {'id': 1, 'name': 'Headphones', 'price': 2500, 'stock': 10},
    {'id': 2, 'name': 'Phone case', 'price': 600, 'stock': 40},
]


@app.get('/')
def home():
    return {'message': 'Welcome to Duka API'}


@app.get('/about')
def about():
    return {'name': 'Lucky', 'message': 'Learning backend at Moringa'}


@app.get('/api/products')
def list_products():
    return jsonify(products), 200


@app.get('/api/products/<int:product_id>')
def get_product(product_id):
    for product in products:
        if product['id'] == product_id:
            return jsonify(product), 200
    return jsonify({'error': 'Product not found'}), 404

@app.post('/api/products')
def create_product():
    data = request.get_json()
    product = {
        'id': len(products) + 1,
        'name': data['name'],
        'price': data['price'],
        'stock': data.get('stock', 0),
    }
    products.append(product)
    return jsonify(product), 201


