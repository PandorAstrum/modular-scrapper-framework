# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "This file is for run the scrapper provided by the name of the scrapper"

This file contains the mechanism to run the scrapper when called
It is called from command line (CMD in Windows or BASH on LINUX)
"""

from scrapy import spiderloader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# from parameters import *
import utility


def general_run(_spider_name, _settings_file):
	_settings_data = utility.readJSON(_settings_file)  # read settings
	_selected_spider = _settings_data[_spider_name]
	_selected_spider_settings = _selected_spider['Settings']
	_project_settings = get_project_settings()
	spider_loader = spiderloader.SpiderLoader.from_settings(_project_settings)
	_spiders = spider_loader.list()
	_spider_classes = [spider_loader.load(name) for name in _spiders]
	_process = CrawlerProcess(_project_settings)
	for _spider in _spider_classes:
		if _spider_name == _spider.name:
			output = utility.get_output_file("scrap")
			_process.settings.update({
				'USER_AGENTS': _selected_spider_settings['User-Agents'],
				'FEED_FORMAT': 'json',
				'FEED_URI': output,
				'LOG_LEVEL': _selected_spider_settings['Log Level'],
				'DELAY': _selected_spider_settings['Delay']
			})
			_process.crawl(_spider, _selected_spider=_selected_spider, _signin=False)

	_process.start()  # the script will block here until the crawling is finished
	_selected_spider['Last Run Time'] = str(utility.get_curr_date_time())
	utility.writeJSON(_settings_file, _settings_data)


def login_run(_spider_name, _settings_file, _username, _password):
	_settings_data = utility.readJSON(_settings_file)  # read settings
	_selected_spider = _settings_data[_spider_name]
	_selected_spider_settings = _selected_spider['Settings']
	_project_settings = get_project_settings()
	spider_loader = spiderloader.SpiderLoader.from_settings(_project_settings)
	_spiders = spider_loader.list()
	_spider_classes = [spider_loader.load(name) for name in _spiders]
	_process = CrawlerProcess(_project_settings)
	for _spider in _spider_classes:
		if _spider_name == _spider.name:
			output = utility.get_output_file("price")
			_process.settings.update({
				'USER_AGENTS': _selected_spider_settings['User-Agents'],
				'FEED_FORMAT': 'json',
				'FEED_URI': output,
				'LOG_LEVEL': _selected_spider_settings['Log Level'],
				'DELAY': _selected_spider_settings['Delay']
			})
			_process.crawl(_spider, _selected_spider=_selected_spider, _signin=True, _username=_username, _password=_password)

	_process.start()  # the script will block here until the crawling is finished
	_selected_spider['Last Run Time'] = str(utility.get_curr_date_time())
	utility.writeJSON(_settings_file, _settings_data)
