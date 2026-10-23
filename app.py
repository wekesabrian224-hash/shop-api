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
