# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Description of this file here"
"""
# -*- coding: utf-8 -*-
from PyInquirer import prompt

import utility
from core.config import cenegy_style
from core.operations import AbsOperation

__all__ = [
	"EditOutput",
	"EditDelay",
	"EditUserAgent",
	"EditLogLevel",
	"EditSiteID",
	"EditURL",
	"EditLoginURL",
	"EditUserName",
	"EditPassword"
]


class EditOutput(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to edit output directory for the selected scrapper
	"""

	@property
	def creation_order(self):
		return 1

	@property
	def _identifier(self):
		return "Edit Output Directory"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_question = [
			{
				'type': 'input',
				'name': 'output',
				'message': 'Enter Output Directory Path :'
			}
		]

		ans = prompt(_question, style=cenegy_style)
		_tmp = ans['output'].replace("\\", "\\")
		_selected_scrapper['Output'] = _tmp
		utility.writeJSON(settings_file, _settings_data)
		print(f"Output Directory Changed to : {ans['output']}")


class EditDelay(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to edit delay
	"""

	@property
	def creation_order(self):
		return 2

	@property
	def _identifier(self):
		return "Edit Delay"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_scrapper_settings = _selected_scrapper['Settings']
		_question = [
			{
				'type': 'input',
				'name': 'delay',
				'message': 'Enter a number (int) :'
			}
		]
		ans = prompt(_question, style=cenegy_style)
		# todo: edit json
		_scrapper_settings['Delay'] = int(ans['delay'])
		utility.writeJSON(settings_file, _settings_data)
		print(f"Spider Delay Set To : {ans['delay']}")


class EditUserAgent(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to add new field and append to json settings
	"""

	@property
	def creation_order(self):
		return 3

	@property
	def _identifier(self):
		return "Edit User Agents"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_scrapper_settings = _selected_scrapper['Settings']
		_question = [
			{
				'type': 'input',
				'name': 'useragents',
				'message': 'Enter New User Agents :'
			}
		]
		ans = prompt(_question, style=cenegy_style)
		_scrapper_settings['User-Agents'] = ans['useragents']
		utility.writeJSON(settings_file, _settings_data)
		print(f"Spider Delay Set To : {ans['delay']}")


class EditLogLevel(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to utilize scrapper and do various things with it
	"""

	@property
	def creation_order(self):
		return 4

	@property
	def _identifier(self):
		return "Edit Log Level"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_scrapper_settings = _selected_scrapper['Settings']
		_question = [
			{
				'type': 'list',
				'name': 'loglevel',
				'message': "Choose a Logging Level :",
				'choices': ["INFO", "DEBUG", "WARNING"]
			}
		]
		ans = prompt(_question, style=cenegy_style)
		_scrapper_settings['Log Level'] = ans['loglevel']
		utility.writeJSON(settings_file, _settings_data)
		print(f"Spider Log Level set To : {ans['loglevel']}")


class EditSiteID(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to utilize scrapper and do various things with it
	"""

	@property
	def creation_order(self):
		return 5

	@property
	def _identifier(self):
		return "Edit Site ID"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_scrapper_settings = _selected_scrapper['Settings']
		_question = [
			{
				'type': 'input',
				'name': 'siteid',
				'message': "Enter New ID number (int):"
			}
		]
		ans = prompt(_question, style=cenegy_style)
		_selected_scrapper['siteID'] = ans["siteid"]
		utility.writeJSON(settings_file, _settings_data)
		print(f"Spider Site ID number changed To : {ans['siteid']}")


class EditURL(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to utilize scrapper and do various things with it
	"""

	@property
	def creation_order(self):
		return 6

	@property
	def _identifier(self):
		return "Edit Site URL"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_question = [
			{
				'type': 'input',
				'name': 'url',
				'message': "Enter New URL :"
			}
		]
		ans = prompt(_question, style=cenegy_style)
		_selected_scrapper['targetURL'] = ans["url"]
		utility.writeJSON(settings_file, _settings_data)
		print(f"Spider Scrapping URL changed To : {ans['url']}")


class EditLoginURL(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to utilize scrapper and do various things with it
	"""

	@property
	def creation_order(self):
		return 7

	@property
	def _identifier(self):
		return "Edit Login URL"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_scrapper_settings = _selected_scrapper['Settings']
		_question = [
			{
				'type': 'input',
				'name': 'loginurl',
				'message': "Enter New ID number (int):"
			}
		]
		ans = prompt(_question, style=cenegy_style)
		_selected_scrapper['loginURL'] = ans["loginurl"]
		utility.writeJSON(settings_file, _settings_data)
		print(f"Spider Login URL changed To : {ans['loginurl']}")


class EditUserName(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to utilize scrapper and do various things with it
	"""

	@property
	def creation_order(self):
		return 8

	@property
	def _identifier(self):
		return "Edit Default Username"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_scrapper_settings = _selected_scrapper['Settings']
		_question = [
			{
				'type': 'input',
				'name': 'deafultusername',
				'message': "Enter New Default Username :"
			}
		]
		ans = prompt(_question, style=cenegy_style)
		_selected_scrapper['username'] = ans["defaultusername"]
		utility.writeJSON(settings_file, _settings_data)
		print(f"Default Username changed To : {ans['defaultusername']}")


class EditPassword(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to utilize scrapper and do various things with it
	"""

	@property
	def creation_order(self):
		return 9

	@property
	def _identifier(self):
		return "Edit Default Password"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_question = [
			{
				'type': 'password',
				'name': 'defaultpassword',
				'message': "Enter Default Password :"
			}
		]
		ans = prompt(_question, style=cenegy_style)
		_selected_scrapper['password'] = ans["defaultpassword"]
		utility.writeJSON(settings_file, _settings_data)
		print(f"Default password changed To : {ans['defaultpassword']}")
