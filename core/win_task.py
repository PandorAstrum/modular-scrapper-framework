# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Description of this file here"
"""
# schtasks /Create /SC HOURLY /TN PythonTask /TR "PATH_TO_PYTHON_EXE PATH_TO_PYTHON_SCRIPT"
import os
from subprocess import Popen, PIPE


# Create Task
# schtasks /create /TN scrapper_test /SC DAILY /TR "C:\Users\Ana Ash\Desktop\skrapy3\project\run.py"

# os.system("start /wait cmd /c {schtasks ?}")


# _p = Popen(['schtasks'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
# _output, _err = _p.communicate(b"stdin")
# rc = _p.returncode
# print(_output)
		# _tmp_spider_list = _output.splitlines()
		# for indx, spider in enumerate(_tmp_spider_list):
		# 	_list.append(str(indx + 1) + ". " + str(spider, 'utf-8'))
		# return _list

import sys
import platform
import imp

print("Python EXE     : " + sys.executable)
_python_path = sys.executable
# _p = Popen(['python', "C:\\Users\\Ana Ash\\Desktop\\skrapy3\\project\\run.py"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
# _output, _err = _p.communicate(b"stdout")
# rc = _p.returncode
# print(_output)
		# _tmp_spider_list = _output.splitlines()
		# for indx, spider in enumerate(_tmp_spider_list):
		# 	_list.append(str(indx + 1) + ". " + str(spider, 'utf-8'))
		# return _list

# TODO: create a batch file to run scrapper
	# TODO: get python path
# set python_path = where python.exe
	#
	# TODO: get the running scripts
	# TODO: Open cmd and run the file
# TODO: schedule to run that batch file
