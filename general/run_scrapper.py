# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "This file is for run the scrapper provided by the name of the scrapper"

This file contains the mechanism to run the scrapper when called
It is called from command line (CMD in Windows or BASH on LINUX)
"""

import json
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders import ArteriorsHome
# from parameters import *
import utility

def loadFields(_scrapper_name):
	with open('settings.json') as json_file:
		_settings_data = json.load(json_file)
		_scrapper_settings = _settings_data[_scrapper_name]
	return _scrapper_settings['fields']


def general_run(_spider_name, _settings_file):
	_project_settings = get_project_settings()
	process = CrawlerProcess(_project_settings)
	# todo: get the settings parameter from the json and set into spider scrapper

	# output = utility.get_output_file("scrap")
	# process.settings.update({
	# 	'FEED_FORMAT': 'json',
	# 	'FEED_URI': output,
	# 	'LOG_LEVEL': 'DEBUG'
	# })
	#
	# # process.crawl(ArteriorsHome.ArteriorshomeSpider,
	# #               _start_urls=_scrapper_settings['targetURL'], _headers=USER_AGENTS, _take_categories=TAKE_CATEGORIES)
	# #
	# # process.start()  # the script will block here until the crawling is finished
	# TODO: edit the json for spiders "Last Run"
	# TODO: edit the json for the spiders

# runscrapper("ArteriorsHome")


def login_run(_scrapperName, _username, _password):
	pass
