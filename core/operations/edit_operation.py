# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Description of this file here"
"""
# -*- coding: utf-8 -*-
from PyInquirer import prompt

import utility
from config import cenegy_style
from core.operations import AbsOperation

__all__ = [
	"CurrentField",
	"EditField",
	"AddField",
	"DeleteField"
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
