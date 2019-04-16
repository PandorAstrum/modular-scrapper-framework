# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "This file is for run the scrapper provided by the name of the scrapper"

This file contains the mechanism to run the scrapper when called
It is called from command line (CMD in Windows or BASH on LINUX)
"""

import json
import sys
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from .spiders import ArteriorsHome
# from parameters import *


def loadFields(_scrapper_name):
	with open('settings.json') as json_file:
		_settings_data = json.load(json_file)
		_scrapper_settings = _settings_data[_scrapper_name]
	return _scrapper_settings['fields']


def runscrapper(_scrapper_name):
	pass
	# load scraper item with the settings
	# according to id get the scrapper settings from json

	# with open('settings.json') as json_file:
	# 	_settings_data = json.load(json_file)
	# 	_scrapper_settings = _settings_data[_scrapper_name]
	# _url = _scrapper_settings['targetURL']
	# _take_price = _scrapper_settings['login']
	# _login_url = _scrapper_settings['loginURL']
	# _username = _scrapper_settings['username']
	# _password = _scrapper_settings['password']
	# _siteId = _scrapper_settings['siteID']
	# # print(_scrapper_settings['fields'])
	# for i in _scrapper_settings['fields']:
	# 	if i['fieldName'] == 'ItemName':
	# 		print(i['Xpath'])

	# _project_settings = get_project_settings()
	# process = CrawlerProcess(_project_settings)

	# todo: get the settings parameter from the json and set into spider scrapper
	_general_settings = _scrapper_settings["Settings"]

	# # output = get_output_filename()
	# process.settings.update({
	# 	'LOG_LEVEL': 'DEBUG',
	# })

	# process.crawl(ArteriorsHome.ArteriorshomeSpider,
	#               _start_urls=_scrapper_settings['targetURL'], _headers=USER_AGENTS, _take_categories=TAKE_CATEGORIES)
	#
	# process.start()  # the script will block here until the crawling is finished
	# TODO: edit the json for spiders "Last Run"
	# TODO: edit the json for the spiders

# runscrapper("ArteriorsHome")