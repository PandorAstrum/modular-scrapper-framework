# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Commands as class object for the cli, also list in __all__ in order to use.
			Default Command is Scrapper Class (Command)"
"""

import re
from PyInquirer import prompt
import utility
from core.config import cenegy_style
from core.questionnaire.abc_question import Director
from core import questionnaire
from .command_lines import AbsCommand
from core.operations.abc_operation import OperationExecutioner, OperationReceiver, AbsOperation
from core.operations import base_operation

__all__ = [
	"Scrapper"
]


class Scrapper(AbsCommand):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This Command is responsible to utilize scrapper and do various things with it
	"""

	@property
	def name(self):
		return 'scrapper'

	@property
	def description(self):
		return 'start scrapper cli'

	def execute(self, args):
		self._receiver.action(self, args)

	def operation(self):
		_director = Director()
		_quest_class = utility.AutoLoader(questionnaire, questionnaire.AbcQuestions, _custom_sort=True)
		_q = _quest_class.initialize_each()
		_questions = []
		for c in _q:
			_director.construct(c)
			_questions.append(_director.get_question())

		_answer = prompt(_questions, style=cenegy_style)

		_spiderName = re.sub(r'\d+[.]\s', '', _answer['spiderName']).strip()  # spider name
		settings_file = utility.get_working_dir() + "\\general\\settings.json"  # the path of the settings file
		settings_data = utility.readJSON(settings_file)  # read settings
		_selected_scrapper = settings_data[_spiderName]  # read the exact scrapper

		_operation_executioner = OperationExecutioner()
		_operation_receiver = OperationReceiver()
		_operation_class = utility.AutoLoader(base_operation, AbsOperation)
		_operation_name = _operation_class.get_names(_property_name="_identifier")
		for _operation in _operation_class.loaded_module.values():
			_operation = _operation(_operation_receiver)
			_operation_executioner.store_operation(_operation)

		for i in _operation_name:
			if _answer['toDo'] == i:
				_operation_executioner.execute_operation(i, settings_file, _spiderName)
