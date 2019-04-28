# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "API To communicate with the flask app"
"""
from __future__ import unicode_literals
# import os
import os
from subprocess import Popen, PIPE
# import json
import requests
from flask import Flask, request, jsonify, make_response, abort
import utility
#
app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'


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


def get_spider_settings(_settings_file, _spider_name):
    _settings_data = utility.readJSON(_settings_file)  # read settings
    return _settings_data[_spider_name]


@app.route('/', methods=['GET'])
def home():
    # get all the spider in a list and display
    _list_of_spiders = get_scrapper(True)
    return jsonify(_list_of_spiders)


@app.route('/jobs', methods=['GET'])
def jobs():
    # get jobs in a jsonify strong simple
    _p = Popen(['curl', '-X', 'GET', 'http://127.0.0.1:6800/listjobs.json?project=general'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    _output, _err = _p.communicate(b"stdin")
    rc = _p.returncode

    return _output


@app.route('/jobs-verbose', methods=['GET'])
def jobs_verbose():
    # get Detailed job list with ui
    _p = Popen(['curl', '-X', 'GET', 'http://127.0.0.1:6800/jobs'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    _output, _err = _p.communicate(b"stdin")
    rc = _p.returncode
    return _output


@app.route('/spider/<spider_name>', methods=['GET'])
def run_products(spider_name):
    # schedule a spider to run
    _spider_name = spider_name
    _selected_spider_settings = get_spider_settings(os.getcwd()+"\\general\\settings.json", _spider_name)
    _tmp_spider_list = get_scrapper()
    if _spider_name not in _tmp_spider_list:
        abort(404)
    else:
        # create output filename with path
        _path = "C:\\Users\\Ana Ash\\Desktop\\skrapy3\\project"
        _filename = utility.get_output_file(_file_name=f"\\{_spider_name}_Products")

        _p = Popen(['curl', 'http://localhost:6800/schedule.json',
                    '-d', 'project=general', '-d', f'spider={_spider_name}',
                    '-d', 'settings=FEED_FORMAT="json"',
                    '-d', 'settings=FEED_STORAGES={"c": "scrapy.extensions.feedexport.FileFeedStorage"}',
                    '-d', f'settings=FEED_URI={_path+_filename}',
                    '-d', f'settings=LOG_LEVEL={_selected_spider_settings["Settings"]["Log Level"]}',
                    '-d', f'settings=DELAY={_selected_spider_settings["Settings"]["Delay"],}',
                    '-d', f'_username=None',
                    '-d', f'_password=None',
                    '-d', f'_signin=False',
                    '-d', f'_start_urls={_selected_spider_settings["targetURL"]}',
                    '-d', f'_siteID={_selected_spider_settings["siteID"]}',
                    '-d', f'_login_url={_selected_spider_settings["loginURL"]}',
                    '-d', f'_customer_id=None',
        ], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        _output, _err = _p.communicate(b"stdin")
        rc = _p.returncode
        # response_data = {
        #     "output": _output["status"],
        #     "success": True,
        #     "status_code": 200
        # }
        return _output, 200


@app.route('/update/<project_name>', methods=["GET"])
def add_version(project_name):
    pass


@app.route('/projects', methods=["GET"])
def get_projects():
    pass


@app.route('/spider/<customer_id>/<spider_name>/<username>/<password>', methods=['GET'])
def run_prices(customer_id, spider_name, username, password):
    _spider_name = spider_name
    _customer_id = customer_id
    _username = username
    _password = password
    # get the list of spiders
    _tmp_spider_list = get_scrapper()
    if _spider_name not in _tmp_spider_list:
        abort(404)
    else:

#          # $ curl
#         # http://localhost:6800/schedule.json -d project= <projectname> -d spider={_spider_name} - d
#         # setting = DOWNLOAD_DELAY = 2 - d
#         # arg1 = val1
        _p = Popen(['curl', 'http://localhost:6800/schedule.json',
                    '-d', 'project=default', '-d', f'spider={_spider_name}'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        _output, _err = _p.communicate(b"stdin")
        rc = _p.returncode


if __name__ == '__main__':
    app.run(debug=True, port=80)



# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=80)
