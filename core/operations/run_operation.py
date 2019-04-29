# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Description of this file here"
"""
from PyInquirer import prompt
import utility
from core.config import cenegy_style
from core.operations import AbsOperation
from general import run_scrapper

__all__ = [
	"GeneralRun",
	"LoginRun"
]


class GeneralRun(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to show current fields
	"""

	@property
	def creation_order(self):
		return 1

	@property
	def _identifier(self):
		return "Scrape Products"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		run_scrapper.scrape_product(_spiderName, settings_file)


class LoginRun(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to edit field's xpath
	"""

	@property
	def creation_order(self):
		return 2

	@property
	def _identifier(self):
		return "Scrape Prices (Required Username, Password, Customer ID)"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_question = [
			{
				'type': 'list',
				'name': 'loginrun',
				'message': 'Login With :',
				'choices' : ["Default", "Provide Now"]
			}
		]

		ans = prompt(_question, style=cenegy_style)
		if ans['loginrun'] == "Default":
			run_scrapper.scrape_price(_spiderName, settings_file,
									_username=_selected_scrapper["username"],
									_password=_selected_scrapper["password"])
		elif ans['loginrun'] == "Provide Now":
			# ask for username and password
			_questionLogin = [
				{
					'type': 'input',
					'name': 'username',
					'message': 'Enter Username or email :',
				},
				{
					'type': 'password',
					'message': 'Enter Password :',
					'name': 'password'
				},
				{
					'type': 'input',
					'message': 'Enter Customer ID :',
					'name': 'customerID'
				}
			]

			ansLogin = prompt(_questionLogin, style=cenegy_style)
			run_scrapper.scrape_price(_spiderName, settings_file,
									_username=ansLogin["username"],
									_password=ansLogin["password"],
									_customerid=ansLogin["customerID"])
