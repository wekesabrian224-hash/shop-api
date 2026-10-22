from flask import Flask, request, jsonify
app = Flask(__name__)

products = [
    {'id': 1, 'name': 'Headphones', 'price': 2500, 'stock': 10},
    {'id': 2, 'name': 'Phone case', 'price': 600, 'stock': 40},
]

def find_product(product_id):
    for product in products:
        if product['id'] == product_id:
            return product
    return None


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
    product = find_product(product_id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product), 200

@app.post('/api/products')
def create_product():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Send a JSON body'}), 400

    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock', 0)

    if not isinstance(name, str) or not name.strip():
        return jsonify({'error': 'name is required'}), 400
    if not isinstance(price, int) or price <= 0:
        return jsonify({'error': 'price must be a positive whole number'}), 400
    if not isinstance(stock, int) or stock < 0:
        return jsonify({'error': 'stock must be 0 or more'}), 400

    product = {
        'id': len(products) + 1,
        'name': name.strip(),
        'price': price,
        'stock': stock,
    }
    products.append(product)
    return jsonify(product), 201


@app.patch('/api/products/<int:product_id>')
def update_product(product_id):
    product = find_product(product_id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json(silent=True) or {}
    if 'name' in data:
        product['name'] = data['name']
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