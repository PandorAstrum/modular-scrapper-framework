# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Commands as class object for the cli, also list in __all__ in order to use.
			Default Command is Scrapper Class (Command)"
"""

import json
import re

from PyInquirer import prompt
import utility
from config import cenegy_style
from core.questionnaire.abc_question import Director
from core import questionnaire
from .command_lines import AbsCommand
import sys


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
		_quest_class = utility.AutoLoader(questionnaire, questionnaire.AbcQuestions, True)
		_q = _quest_class.initialize_each()
		_questions = []
		for c in _q:
			_director.construct(c)
			_questions.append(_director.get_question())

		_answer = prompt(_questions, style=cenegy_style)
		_spiderName = re.sub(r'\d+[.]\s', '', _answer['spiderName'])
		# TODO: load settings
		# with open('settings.json') as json_file:
		# 	_settings_data = json.load(json_file)

		# TODO: depending on question start another cli session or delegate extra commands
