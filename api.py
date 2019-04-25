# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Description of this file here"
"""
from flask import Flask, request, jsonify, make_response
# from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
# import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
#
# db = SQLAlchemy(app)
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     public_id = db.Column(db.String(50), unique=True)
#     name = db.Column(db.String(50))
#     password = db.Column(db.String(80))
#     admin = db.Column(db.Boolean)
#
# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(50))
#     complete = db.Column(db.Boolean)
#     user_id = db.Column(db.Integer)

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
#
#         if not token:
#             return jsonify({'message' : 'Token is missing!'}), 401
#
#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'])
#             current_user = User.query.filter_by(public_id=data['public_id']).first()
#         except:
#             return jsonify({'message' : 'Token is invalid!'}), 401
#
#         return f(current_user, *args, **kwargs)
#
#     return decorated


@app.route('/spider/<spider_name>', methods=['GET'])
def run_products(spider_name):
    _spider_name = spider_name
    # get settings file
    # call run scrapper for product
    # dump the data and get everything from it
    # json loads return
    return jsonify({'Spider Name': _spider_name})

@app.route('/spider/<customer_id>/<spider_name>/<username>/<password>', methods=['GET'])
def run_prices(customer_id, spider_name, username, password):
    _spider_name = spider_name
    _customer_id = customer_id
    _username = username
    _password = password

    return jsonify([{'Spider name': _spider_name,
                    'Customer id': _customer_id,
                    'Username': _username,
                    'Password': _password},
                    {'Spider name': _spider_name,
                     'Customer id': _customer_id,
                     'Username': _username,
                     'Password': _password}])

if __name__ == '__main__':
    app.run(debug=True)
