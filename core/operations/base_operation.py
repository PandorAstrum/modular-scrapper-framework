# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Description of this file here"
"""
from PyInquirer import prompt
from core.questionnaire.abc_question import Director
import utility
from core.operations.abc_operation import AbsOperation, OperationExecutioner, OperationReceiver
from core.operations import edit_operation, run_operation, deploy_operation
from config import cenegy_style

__all__ = [
	"Status",
	"Edit",
	"Run",
	"Deploy"
]


class Status(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to show selected spiders status
	"""

	@property
	def creation_order(self):
		return 1

	@property
	def _identifier(self):
		return "Status"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name  # spider name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_scrapper_settings = _selected_scrapper['Settings']
		print(f"Spider Name : {_spiderName}")
		print(f"Scrapping URL : {_selected_scrapper['targetURL']}")
		print(f"Site ID: {_selected_scrapper['siteID']}")
		print(f"Scheduled Status : {_selected_scrapper['Scheduled']}")
		print(f"Deployed Status : {_selected_scrapper['Deployed']}")
		print(f"Last Time Scrapper run : {_selected_scrapper['Last Run Time']}")
		print(f"Any Changes Detected : ")
		print(f"Spider User Agents : {_scrapper_settings['User-Agents']}")
		print(f"Spider Log Level : {_scrapper_settings['Log Level']}")
		print(f"Spider Delay : {_scrapper_settings['Delay']} Seconds")
		print(f"Spider Result output Directory : {_selected_scrapper['Output']}")


class Edit(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to edit field of the selected scrapper
	"""

	@property
	def creation_order(self):
		return 2

	@property
	def _identifier(self):
		return "Edit"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name  # spider name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_director = Director()
		_quest_class = utility.AutoLoader(edit_operation, AbsOperation)
		_choices = _quest_class.get_names(_property_name="_identifier")
		_questions = [
			{
				'type': 'list',
				'name': 'edit',
				'message': f'Editing {_spiderName}:',
				'choices': _choices
			}
		]

		_answer = prompt(_questions, style=cenegy_style)
		_operation_executioner = OperationExecutioner()
		_operation_receiver = OperationReceiver()
		_operation_class = utility.AutoLoader(edit_operation, AbsOperation)
		_operation_name = _operation_class.get_names(_property_name="_identifier")
		for _operation in _operation_class.loaded_module.values():
			_operation = _operation(_operation_receiver)
			_operation_executioner.store_operation(_operation)

		for i in _operation_name:
			if _answer['edit'] == i:
				_operation_executioner.execute_operation(i, settings_file, _spiderName)


class Run(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to run the selected scrapper
	"""

	@property
	def creation_order(self):
		return 3

	@property
	def _identifier(self):
		return "Run"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name  # spider name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]

		_director = Director()
		_quest_class = utility.AutoLoader(run_operation, AbsOperation)
		_choices = _quest_class.get_names(_property_name="_identifier")
		_questions = [
			{
				'type': 'list',
				'name': 'run',
				'message': f'Run {_spiderName}:',
				'choices': _choices
			}
		]
		_answer = prompt(_questions, style=cenegy_style)
		_operation_executioner = OperationExecutioner()
		_operation_receiver = OperationReceiver()
		_operation_class = utility.AutoLoader(run_operation, AbsOperation)
		_operation_name = _operation_class.get_names(_property_name="_identifier")
		for _operation in _operation_class.loaded_module.values():
			_operation = _operation(_operation_receiver)
			_operation_executioner.store_operation(_operation)

		for i in _operation_name:
			if _answer['run'] == i:
				_operation_executioner.execute_operation(i, settings_file, _spiderName)


class Deploy(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to deploy selected scrapper
	"""

	@property
	def creation_order(self):
		return 4

	@property
	def _identifier(self):
		return "Deploy"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name  # spider name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]

		_director = Director()
		_quest_class = utility.AutoLoader(deploy_operation, AbsOperation)
		_choices = _quest_class.get_names(_property_name="_identifier")
		_questions = [
			{
				'type': 'list',
				'name': 'deploy',
				'message': f'Deploy {_spiderName}:',
				'choices': _choices
			}
		]
		_answer = prompt(_questions, style=cenegy_style)
		_operation_executioner = OperationExecutioner()
		_operation_receiver = OperationReceiver()
		_operation_class = utility.AutoLoader(deploy_operation, AbsOperation)
		_operation_name = _operation_class.get_names(_property_name="_identifier")
		for _operation in _operation_class.loaded_module.values():
			_operation = _operation(_operation_receiver)
			_operation_executioner.store_operation(_operation)

		for i in _operation_name:
			if _answer['deploy'] == i:
				_operation_executioner.execute_operation(i, settings_file, _spiderName)
