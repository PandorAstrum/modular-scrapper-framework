# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Description of this file here"
"""
# -*- coding: utf-8 -*-
from PyInquirer import prompt

import utility
from core.config import cenegy_style
from core.operations import AbsOperation, scrapper_settings_operation, OperationExecutioner, OperationReceiver
from core.questionnaire.abc_question import Director

__all__ = [
	"CurrentField",
	"EditField",
	"AddField",
	"DeleteField",
	"EditSettings",
	"Default"
]


class CurrentField(AbsOperation):
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
		return "Current Fields"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_all_field = _selected_scrapper['fields']
		print(f"Total Field = {len(_all_field)}")
		for _a in _all_field:
			print(f"Field Name : {_a['fieldName']}, Field XPATH : {_a['Xpath']}")


class EditField(AbsOperation):
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
		return "Edit Field"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_all_field = _selected_scrapper['fields']
		_fieldNames = []
		for _a in _all_field:
			_fieldNames.append(_a['fieldName'])
		_questionSelect = [
			{
				'type': 'rawlist',
				'name': 'selectField',
				'message': 'Select A field to Edit',
				'choices': _fieldNames
			}
		]
		_answerSelect = prompt(_questionSelect, style=cenegy_style)
		for _a in _all_field:
			if _answerSelect['selectField'] == _a['fieldName']:
				_questionEdit = [
					{
						'type': 'input',
						'name': 'fieldXpath',
						'message': 'Enter New Field Xpath',
					}
				]
				_answerEdit = prompt(_questionEdit, style=cenegy_style)
				_a['Xpath'] = _answerEdit['fieldXpath']
				utility.writeJSON(settings_file, _settings_data)
				print(f"{_answerSelect['selectField']} Xpath Changed to {_answerEdit['fieldXpath']}")


class AddField(AbsOperation):
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
		return "Add Field"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_questAddField = [
			{
				'type': 'input',
				'name': 'fieldName',
				'message': 'Name the Field or Key',
			},
			{
				'type': 'input',
				'name': 'fieldXpath',
				'message': 'XPATH to the field',
			}
		]
		_answerAddField = prompt(_questAddField, style=cenegy_style)
		_data = {
			"fieldName": f"{_answerAddField['fieldName']}",
			"Xpath": f"{_answerAddField['fieldXpath']}"
		}
		_selected_scrapper['fields'].append(_data)
		utility.writeJSON(settings_file, _settings_data)
		print(f"{_data['fieldName']} Field Added")


class DeleteField(AbsOperation):
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
		return "Delete Field"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_all_field = _selected_scrapper['fields']
		_fieldNames = []
		for _a in _all_field:
			_fieldNames.append(_a['fieldName'])
		_questionSelect = [
			{
				'type': 'rawlist',
				'name': 'selectField',
				'message': 'Select A field name to delete',
				'choices': _fieldNames
			}
		]
		_answerSelect = prompt(_questionSelect, style=cenegy_style)
		for _a in _all_field:
			if _answerSelect['selectField'] == _a['fieldName']:
				_questionDelete = [
					{
						'type': 'confirm',
						'message': f"Do you want to Delete {_answerSelect['selectField']}?",
						'name': 'delete',
						'default': True,
					}
				]
				_answerDelete = prompt(_questionDelete, style=cenegy_style)
				if _answerDelete['delete']:
					new_all_field = []
					for x in _all_field:
						if not _answerSelect['selectField'] == x['fieldName']:
							new_all_field.append(x)
					# _all_field = [x for x in _all_field if not (_answerSelect['selectField'] == _a.get('fieldName'))]

					_selected_scrapper['fields'] = new_all_field
					utility.writeJSON(settings_file, _settings_data)
					print(f"{_answerSelect['selectField']} Deleted")


class EditSettings(AbsOperation):
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
		return "Edit Settings"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		_scrapper_settings = _selected_scrapper['Settings']
		_director = Director()
		_quest_class = utility.AutoLoader(scrapper_settings_operation, AbsOperation)
		_choices = _quest_class.get_names(_property_name="_identifier")
		_questions = [
			{
				'type': 'rawlist',
				'name': 'settings',
				'message': f'Changing Settings For {_spiderName}:',
				'choices': _choices
			}
		]

		_answer = prompt(_questions, style=cenegy_style)
		_operation_executioner = OperationExecutioner()
		_operation_receiver = OperationReceiver()
		_operation_class = utility.AutoLoader(scrapper_settings_operation, AbsOperation)
		_operation_name = _operation_class.get_names(_property_name="_identifier")
		for _operation in _operation_class.loaded_module.values():
			_operation = _operation(_operation_receiver)
			_operation_executioner.store_operation(_operation)

		for i in _operation_name:
			if _answer['settings'] == i:
				_operation_executioner.execute_operation(i, settings_file, _spiderName)


class Default(AbsOperation):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to show current fields
	"""

	@property
	def creation_order(self):
		return 6

	@property
	def _identifier(self):
		return "Default Settings"

	def execute(self, operation_name, settings_file, selected_spider_name):
		self._operation_receiver.action(self, operation_name, settings_file, selected_spider_name)

	def operation(self, settings_file, selected_spider_name):
		_spiderName = selected_spider_name
		_settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = _settings_data[_spiderName]
		questions = [
			{
				'type': 'confirm',
				'message': 'This will revert back the Spider Settings to Default. Do you want to continue?',
				'name': 'default',
				'default': True,
			}
		]

		answers = prompt(questions, style=cenegy_style)
		if answers['default']:
			default_json = {"ArteriorsHome":
								{
									"_id": 1,
									"targetURL": "https://www.arteriorshome.com/shop",
									"loginURL": "https://www.arteriorshome.com/customer/account/login/",
									"username": "michael@masmarkre.com",
									"password": "arteriors",
									"siteID": 3,
									"fields":
										[
											{
												"fieldName": "ItemName",
												"Xpath": '//div[@class="product-name"]/h1/text()'
											},
											{
												"fieldName": "SKU",
												"Xpath": '//span[@id="spansku"]/text()'
											},
											{
												"fieldName": "ItemDescription",
												"Xpath": '//div[@id="description"]/text()'
											},
											{
												"fieldName": "Dimension",
												"Xpath": '//li[@id="dimensions"]/span[@class="data"]/span[@class="product-diamen"]/text()'
											},
											{
												"fieldName": "Photos",
												"Xpath": '//li[@class="item"]/a/img/@src'
											},
											{
												"fieldName": "Category",
												"Xpath": '//div[@class="category"]'
											}
										],
									"Scheduled": False,
									"Scheduled Time": "",
									"Deployed": False,
									"Deployed to": "",
									"Last Run Time": "",
									"Changes Detected at field": "",
									"Settings":
										{
											"Log Level": "INFO",
											"Delay": 0,
											"User-Agents": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.3"
										},
									"Output": "C:\\Users\\Ana Ash\\Desktop\\skrapy3\\project"
								}
			}

			utility.writeJSON(settings_file, default_json)
			print("Spider Settings Back to Default")
		else:
			print("Back to Default Cancelled")
