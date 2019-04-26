# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Description of this file here"
"""
from __future__ import unicode_literals

import os
from subprocess import Popen, PIPE
import json
import requests
from flask import Flask, request, jsonify, make_response
import utility
from general.run_scrapper import scrape_product, scrape_price
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


def get_scrapper(with_index=False):
    _p = Popen(['scrapy', 'list'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    _output, _err = _p.communicate(b"stdin")
    rc = _p.returncode
    _spider_list = _output.splitlines()
    _tmp_spider_list = []
    if not with_index:
        for spider in _spider_list:
            _tmp_spider_list.append(str(spider, 'utf-8'))
    else:
        for indx, spider in enumerate(_spider_list):
            _tmp_spider_list.append(str(indx + 1) + ". " + str(spider, 'utf-8'))
    return _tmp_spider_list


@app.route('/', methods=['GET'])
def home():
    # get all the spider in a list and display
    _tmp_spider_list = get_scrapper(True)
    return jsonify(_tmp_spider_list)


@app.route('/spider/<spider_name>', methods=['GET'])
def run_products(spider_name):
    _spider_name = spider_name
    _tmp_spider_list = get_scrapper()

    if _spider_name not in _tmp_spider_list:
        return jsonify({"Error": f"No Spider Named {_spider_name}"})
    else:
        params = {
            "_username": None,
            "_password": None,
            "_signin": False,
            "_spider": _spider_name,
            "spider_name": _spider_name,
            "start_requests": True
        }
        # async run or pool here
        response = requests.get('http://localhost:9080/crawl.json', params)
        _data = json.loads(response.text)

        if _data['status'] == 'ok':
            # call back when done request post to https://vendacartapi.azurewebsites.net/api/productlistimport
            # return dumped json when done to file C:\vendart\products\new
            _filename = utility.get_output_file(_file_name=f"\\{_spider_name}_product")
            utility.writeJSON(os.getcwd()+_filename, _data['items'])
            return jsonify(_data)
        else:
            return jsonify('something went wrong')


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
        # settings_file = utility.get_working_dir() + "/general/settings.json"  # the path of the settings file
        # settings_data = utility.readJSON(settings_file)  # read settings
        # _selected_scrapper = settings_data[_spider_name]  # read the exact scrapper
        params = {
            "_username": _username,
            "_password": _password,
            "_signin": True,
            '_spider': _spider_name,
            'spider_name': _spider_name,
        }
        # async run or pool here
        response = requests.get('http://localhost:9080/crawl.json', params)
        _data = json.loads(response.text)
        # call back when done request post to https://vendacartapi.azurewebsites.net/api/pricing
        # return dumped json when done to file C:\vendart\pricing\new

        if _data['status'] == 'ok':
            _filename = utility.get_output_file(_file_name=f"\\{_spider_name}_product")
            utility.writeJSON(os.getcwd() + _filename, _data['items'])
            return jsonify(_data['items'])
        else:
            return jsonify('something went wrong')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
