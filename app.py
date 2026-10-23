from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop-api.db'

from app import db, Product, Category

electronics = Category(name='Electronics')
fashion = Category(name='Fashion')

db.session.add_all([
    Product(name='Headphones', price=2500, stock=10, category=electronics),
    Product(name='Phone case', price=600, stock=40, category=electronics),
    Product(name='Kitenge shirt', price=1800, stock=25, category=fashion),
    Product(name='Notebook', price=300, stock=20),
])
db.session.commit()




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