from flask import Flask, jsonify

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