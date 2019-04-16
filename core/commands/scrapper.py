# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Commands as class object for the cli, also list in __all__ in order to use.
			Default Command is Scrapper Class (Command)"
"""

import re

from PyInquirer import prompt
import utility
from config import cenegy_style
from core.questionnaire.abc_question import Director
from core import questionnaire
from .command_lines import AbsCommand

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
		_spiderName = re.sub(r'\d+[.]\s', '', _answer['spiderName']).strip()

		# TODO: load settings
		settings_file = utility.get_working_dir() + "\\general\\settings.json"

		settings_data = utility.readJSON(settings_file)
		_selected_scrapper = settings_data[_spiderName]

		# TODO: depending on question start another cli session or delegate extra commands
		if _answer['toDo'].lower() == 'status':
			print(f"Scrapping URL : {_selected_scrapper['targetURL']}")
			print(f"Site ID: {_selected_scrapper['siteID']}")
			print(f"Scheduled Status : {_selected_scrapper['Scheduled']}")
			print(f"Deployed Status : {_selected_scrapper['Deployed']}")
			print(f"Last Time Scrapper run : {_selected_scrapper['Last Run Time']}")
			print(f"Any Changes Detected : ")
		elif _answer['toDo'].lower() == 'edit scrapper':
			print("Editing loop begins")
		elif _answer['toDo'].lower() == 'run now':
			print("calling scrapper runner here and updates json")
		elif _answer['toDo'].lower() == 'deploy':
			print("deploying to")
		elif _answer['toDo'].lower() == 'schedule':
			print("scheduling to run later")
