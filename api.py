# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Description of this file here"
"""
from __future__ import unicode_literals
from subprocess import Popen, PIPE
import json
import requests
from flask import Flask, request, jsonify, make_response

import utility
from general.run_scrapper import scrape_product, scrape_price

# from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
# import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'

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


def get_scrapper():
    _p = Popen(['scrapy', 'list'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    _output, _err = _p.communicate(b"stdin")
    rc = _p.returncode
    _spider_list = _output.splitlines()
    _tmp_spider_list = []
    for spider in _spider_list:
        _tmp_spider_list.append(str(spider, 'utf-8'))
    return _tmp_spider_list


@app.route('/', methods=['GET'])
def home():
    # get all the spider in a list and display
    _tmp_spider_list = get_scrapper()
    _list = []
    for indx, spider in enumerate(_tmp_spider_list):
        _list.append(str(indx + 1) + ". " + str(spider, 'utf-8'))
    return jsonify(_list)


@app.route('/spider/<spider_name>', methods=['GET'])
def run_products(spider_name):
    _spider_name = spider_name
    _tmp_spider_list = get_scrapper()

    if _spider_name not in _tmp_spider_list:
        return jsonify({"Error": f"No Spider Named {_spider_name}"})
    else:
        # get settings file
        settings_file = utility.get_working_dir() + "/general/settings.json"  # the path of the settings file
        settings_data = utility.readJSON(settings_file)  # read settings
        _selected_scrapper = settings_data[_spider_name]  # read the exact scrapper
        # call run scrapper for product
        params = {
        "_username": None,
        "_password": None,
        "_signin": False,
        '_spider': _spider_name,
        'spider_name': _spider_name,
        'start_requests': True
        }
        # http: // 127.0
        # .0
        # .1: 5000 / spider / test_customer_id / ArteriorsHome / michael @ masmarkre.com / arteriors
        response = requests.get('http://localhost:9080/crawl.json', params)
        # scrape_product(_spider_name, settings_file)
        # dump the data and get everything from it
        # json loads return
        return jsonify(response.text)


@app.route('/spider/<customer_id>/<spider_name>/<username>/<password>', methods=['GET'])
def run_prices(customer_id, spider_name, username, password):
    _spider_name = spider_name
    _customer_id = customer_id
    _username = username
    _password = password
    # get the list of spiders
    _tmp_spider_list = get_scrapper()
    if _spider_name not in _tmp_spider_list:
        return jsonify({"Error": f"No Spider Named {_spider_name}"})
    else:
        # get settings file
        settings_file = utility.get_working_dir() + "/general/settings.json"  # the path of the settings file
        settings_data = utility.readJSON(settings_file)  # read settings
        _selected_scrapper = settings_data[_spider_name]  # read the exact scrapper

        # self._selected_spider = kwargs.get('_selected_spider')
        # self._username = kwargs.get("_username")
        # self._password = kwargs.get("_password")
        # self._login = kwargs.get("_signin")
        # self._take_price = kwargs.get("_signin")
        # self.headers = self._selected_spider['Settings']['User-Agents']
        # self._login_url = self._selected_spider['loginURL']
        # self.siteID = self._selected_spider['siteID']
        # self.start_urls = [self._selected_spider['targetURL']]
        params = {
            '_spider': _spider_name,

            '_selected_spider': _selected_scrapper,
            '_username': _username,
            '_password': _password,
            '_signin': True,
            '_customerid': _customer_id
        }
        # http: // 127.0
        # .0
        # .1: 5000 / spider / test_customer_id / ArteriorsHome / michael @ masmarkre.com / arteriors
        response = requests.get('http://localhost:5000/crawl.json?_spider=ArteriorsHome/&_signin=True', params)
        # data = json.loads(response.text)
        # result = '\n'.join('<p><b>{}</b> - {}</p>'.format(item['author'], item['text'])
        #                    for item in data['items'])
        return response.text
        # call run scrapper for product
        # _data = scrape_price(_spider_name, settings_file, _username, _password, _customer_id)

        # return jsonify(_data)


if __name__ == '__main__':
    app.run(debug=True)
