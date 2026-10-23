from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///duka.db'

db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    products = db.relationship('Product', backref='category', lazy=True)

    def to_dict(self):
        return {'id': self.id, 'name': self.name}


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock,
            'category_id': self.category_id,
            'category': self.category.name if self.category else None,
        }

    def __repr__(self):
        return f'<Product {self.id}: {self.name}>'


with app.app_context():
    db.create_all()


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


def check_category(data):
    if 'category_id' not in data or data['category_id'] is None:
        return None

    category_id = data['category_id']
    if isinstance(category_id, bool) or not isinstance(category_id, int):
        return 'category_id must be a whole number'
    if db.session.get(Category, category_id) is None:
        return 'category does not exist'
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
    search = request.args.get('search', '').strip()

    query = Product.query
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    items = query.order_by(Product.id).all()
    return jsonify([item.to_dict() for item in items]), 200


@app.get('/api/products/<int:product_id>')
def get_product(product_id):
    product = db.session.get(Product, product_id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_dict()), 200


@app.post('/api/products')
def create_product():
    data = request.get_json(silent=True)

    problem = validate_product(data) or check_category(data)
    if problem:
        return jsonify({'error': problem}), 400

    product = Product(
        name=data['name'].strip(),
        price=data['price'],
        stock=data.get('stock', 0),
        category_id=data.get('category_id'),
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201


@app.patch('/api/products/<int:product_id>')
def update_product(product_id):
    product = db.session.get(Product, product_id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json(silent=True)
    problem = validate_product(data, partial=True) or check_category(data)
    if problem:
        return jsonify({'error': problem}), 400

    if 'name' in data:
        product.name = data['name'].strip()
    if 'price' in data:
        product.price = data['price']
    if 'stock' in data:
        product.stock = data['stock']
    if 'category_id' in data:
        product.category_id = data['category_id']

    db.session.commit()
    return jsonify(product.to_dict()), 200


@app.delete('/api/products/<int:product_id>')
def delete_product(product_id):
    product = db.session.get(Product, product_id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return '', 204


@app.get('/api/categories')
def list_categories():
    categories = Category.query.order_by(Category.name).all()
    return jsonify([c.to_dict() for c in categories]), 200


@app.post('/api/categories')
def create_category():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Send a JSON object as the body'}), 400

    name = data.get('name')
    if not isinstance(name, str) or not name.strip():
        return jsonify({'error': 'name is required'}), 400
    name = name.strip()

    existing = Category.query.filter(
        db.func.lower(Category.name) == name.lower()
    ).first()
    if existing:
        return jsonify({'error': 'Category already exists'}), 409

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Route not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405