#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    #make an empty list
    bakeries = []
    #loop db query to get all bakeries
    for bakery in Bakery.query.all():
        #build the body of the bakery dict
        bakery_dict = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at
        }
        #append to the empty list
        bakeries.append(bakery_dict)

    #make the response
    response = make_response(
        jsonify(bakeries), 
        200,
        {"Content-Type": 'application/json'})
    #return the response
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at
        }

    response = make_response(
        jsonify(bakery_dict), 
        200)
    
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    prices = []
    for good in BakedGood.query.order_by(desc(BakedGood.price)).all():
        good_dict = {
            'id': good.id,
            'name': good.name,
            'price': good.price,
            'created_at': good.created_at
        }
        prices.append(good_dict)

    response = make_response(prices, 200)
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    good = BakedGood.query.order_by(desc(BakedGood.price)).first()
    good_dict = {
            'id': good.id,
            'name': good.name,
            'price': good.price,
            'created_at': good.created_at
        }

    response = make_response(
        jsonify(good_dict), 
        200)
    
    return response
    

    return ''

if __name__ == '__main__':
    app.run(port=5554, debug=True)
