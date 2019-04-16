# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Utility File to help various thing"
"""

import os
import glob
import json
from datetime import datetime
from inspect import getmembers, isclass, isabstract


def get_curr_date_time(_strft="%Y_%b_%d_%H.%M.%S"):
    """
    functions for getting current time
    :param _strft: format to use on time
    :return: datetime now with provided format
    """
    return datetime.now().strftime(_strft)


def get_output_file(_file_name='', _extension="json"):
    """
    function for get the output file name and format
    :param _file_name: string
    :param _extension: string
    :return: string
    """
    return f"{_file_name}.{_extension}"


def get_all_variable(_package):
    return [attr for attr in dir(_package) if
               not callable(getattr(_package, attr)) and not attr.startswith("__")]


class AutoLoader(object):
    loaded_module = {}

    def __init__(self, _package, _abs_cls, _custom_sort):
        self.load_module(_package, _abs_cls, _custom_sort)

    def load_module(self, _package, _abs_cls, _custom_sort=False):
        self.loaded_module= {}
        classes = getmembers(_package, lambda m: isclass(m) and not isabstract(m))  # make sure its not abstract class

        for name, _type in classes:
            if isclass(_type) and issubclass(_type, _abs_cls):
                self.loaded_module.update([[name, _type]])

        if _custom_sort:
            self.rearrange()

    def initialize(self, _cls_str):
        for key, value in self.loaded_module.items():
            if key.lower() == _cls_str.lower():
                return self.loaded_module[key]()

    def rearrange(self):
        local_ = {}
        for key, value in self.loaded_module.items():
            _order = getattr(self.loaded_module[key](), 'creation_order')
            local_[key] = _order
            local_ = {k: v for k, v in sorted(local_.items(), key=lambda x: x[1])}
        for key, value in local_.items():
            local_[key] = self.loaded_module[key]
        self.loaded_module = local_

    def get_loaded_modules(self):
        return self.loaded_module

    def get_names(self, _lower=False, _property_name=""):
        _tmp = []
        if _property_name != "":
            for key, value in self.loaded_module.items():
                _prop = getattr(self.loaded_module[key](None), _property_name)
                _tmp.append(_prop)
            return _tmp
        else:
            for i in self.loaded_module.values():
                if _lower:
                    _tmp.append(i.__name__.lower())
                else:
                    _tmp.append(i.__name__)
            return _tmp

    def create_instance(self, question_cls):
        if question_cls in self.loaded_module:
            return self.loaded_module[question_cls]()
        else:
            return None

    def initialize_each(self):
        tmp = []
        for i in self.loaded_module.values():
            tmp.append(i())
        return tmp


def create_py(_file_path):
    with open(_file_path, 'w') as python_file:
        python_file.write("# -*- coding: utf-8 -*-" + "\n")


def modify_py(_file_path, _template):
    with open(_file_path, 'a') as python_file:
        python_file.write(_template + "\n")


def search_file(_path, _file, _format):
    """
    function for searching json file ends with bot in a specified folder
    :param _path: path <STRING> to look for the json file
    :param _file: <STRING> name of file with extension
    :param _format: <STRING> 'path' or 'files'
    :return: <LIST> of dirs or files
    """
    _dir = _path
    _files = glob.glob(os.path.join(_dir, _file))
    if _format == "path":
        return _files
    elif _format == "files":
        _tmp = []
        for _f in _files:
           _tmp.append( _f.replace(_dir,''))
        return _tmp


def readJSON(_filepath):
    with open(_filepath) as json_file:
        data = json.load(json_file)
    return data


def writeJSON(_filepath, _data):
    with open(_filepath, 'w') as outfile:
        json.dump(_data, outfile)


def get_this_directory():
    _file_directory = os.path.dirname(__file__)
    return _file_directory


def create_directory(_name):
    # print(os.getcwd())
    # this_file_dir = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # print(this_file_dir)
    print(ROOT_DIR)
    print(os.path.split(os.environ['VIRTUAL_ENV'])[0])
    # if not os.path.exists('shift_graphs'):
    #     os.mkdir('shift_graphs')


def get_working_dir():
    return os.getcwd()
