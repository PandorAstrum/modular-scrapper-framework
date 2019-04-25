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
import utility


def scrape_product(_spider_name, _settings_file):
	"""
	Functions to call Spider to crawl without login
	:param _spider_name: <str> name of the spider
	:param _settings_file: <path> to json settings file
	:return:
	"""
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
			_filename = utility.get_output_file(_file_name=f"{_spider_name}_product")
			output = _filename
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


def scrape_price(_spider_name, _settings_file, _username, _password, _customerid):
	"""
	Function to call spider with Login
	:param _spider_name: <str> name of the spider
	:param _settings_file: <path> to json settings file
	:param _username: <str> username to login
	:param _password: <str> password to log in
	:param _customerid: <str> customer id
	:return:
	"""
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
			_filename = utility.get_output_file(_file_name=f"{_customerid}_{_spider_name}_price")
			_process.settings.update({
				'USER_AGENTS': _selected_spider_settings['User-Agents'],
				'FEED_FORMAT': 'json',
				'FEED_URI': _filename,
				'LOG_LEVEL': _selected_spider_settings['Log Level'],
				'DELAY': _selected_spider_settings['Delay']
			})
			_process.crawl(_spider, _selected_spider=_selected_spider,
							_signin=True,
							_username=_username,
							_password=_password,
							_customerid=_customerid)

	_process.start()  # the script will block here until the crawling is finished
	_selected_spider['Last Run Time'] = str(utility.get_curr_date_time())
	utility.writeJSON(_settings_file, _settings_data)
