# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Default Command for the cli"
"""

import json
import re
from subprocess import Popen, PIPE

from PyInquirer import prompt, Token, prompt, Separator

import utility
from config import cenegy_style
from core.questionnaire.abc_question import Director
from core import questionnaire
from core.questionnaire.scrapy_questions import SpiderSelectQuest
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
		_questions = _quest_class.get_names()
		_q = _quest_class.initialize_each()
		_quest = []
		for c in _q:

			_director.construct(c)
			_quest.append(_director.get_question())
		# for _q in _questions:
		# 	_director.construct(_q())
		# _question = [_director.get_question()]
		_answer = prompt(_quest, style=cenegy_style)
		# TODO: load settings
		# with open('settings.json') as json_file:
		# 	_settings_data = json.load(json_file)

		# TODO: auto load all question

		# _p = Popen(['scrapy', 'list'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		# _output, _err = _p.communicate(b"stdin")
		# rc = _p.returncode
		# _tmp_spider_list = _output.splitlines()
		# _spider_list = []
		# for indx, spider in enumerate(_tmp_spider_list):
		# 	_spider_list.append(str(indx + 1) + ". " + str(spider, 'utf-8'))

		# questions = [
		# 	# first questions
		# 	{
		# 		'type': 'list',
		# 		'name': 'spiderName',
		# 		'message': 'Select A Spider',
		# 		'choices': _spider_list
		# 	},
		# 	# second question
		# 	{
		# 		'type': 'list',
		# 		'name': 'lol',
		# 		'message': 'What to do with the Spider',
		# 		'choices': [
		# 			'Status',
		# 			'Add Field',
		# 			'Edit Field',
		# 			'Run Now',
		# 			'Schedule',
		# 			'Deploy'
		# 		]
		# 	}
		# ]
		#
		# answers = prompt(questions, style=matrix_style)
		# _spiderName = re.sub(r'\d+[.]\s', '', answers['spiderName'])

		# second part question answer
		# Depending on answers run different commands
		# if answers['lol'] == "Status":
		# 	# TODO: get settings of the scrapper
		#
		#
		# 	print("Current status of the selected spider")
		# elif answers["lol"] == "Run Now":
		# 	print("Call the run_scrapper script")
		# elif answers["lol"] == "Add Field":
		# 	print("Add New Field To the Scrapper")
		# elif answers["lol"] == "Edit Field":
		# 	print("Edit The field")
		# elif answers["lol"] == "Schedule":
		# 	print("Scheduled to run at ")
		# elif answers["lol"] == "Deploy":
		# 	print("Deploying to heroku")
