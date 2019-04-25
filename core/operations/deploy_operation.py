# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Description of this file here"
"""

from PyInquirer import prompt
import utility
from config import cenegy_style
from core.operations import AbsOperation

__all__ = [
	"ScrappingHubDeploy",
	"WinDeploy"
]


class ScrappingHubDeploy(AbsOperation):
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
		return "Deploy to Scrapping Hub"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		print("call deploy to scrapping hub")


class WinDeploy(AbsOperation):
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
		return "Schedule Task Win 64"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		# get spider name
		# settings file
		# TODO: choice general run or login run

		# TODO: selected spider name
		# TODO:
		# TODO:
		# TODO:
		# TODO:
		# TODO:
		print("call schedule task")
