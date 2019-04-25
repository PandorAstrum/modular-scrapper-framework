# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Description of this file here"
"""
import os
import sys
from general import auto_runner
_python_path = sys.executable
directory = os.getcwd()

file_path = os.path.abspath(auto_runner.__file__)
with open(os.path.join(directory, 'output_file.bat'), 'w') as OPATH:
    OPATH.writelines([
        "FOR /f %%p in ('where python') do SET PYTHONPATH=%%p \n",
        "ECHO %PYTHONPATH% \n"
        '@echo off\n',
        f'"{_python_path}" "{file_path}" %* \n',
        'pause'])
