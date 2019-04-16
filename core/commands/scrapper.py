# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Default Command for the cli"
"""

import json
from subprocess import Popen, PIPE

from PyInquirer import prompt, Token, prompt, Separator

from config import matrix_style
from core.questionnaire.abc_question import Director
from core.questionnaire.scrapy_questions import SpiderSelectQuest
from .command_lines import AbsCommand
import sys


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
		with open('settings.json') as json_file:
			_settings_data = json.load(json_file)

		questions = [
			# first questions
			{
				'type': 'list',
				'name': 'spiderName',
				'message': 'Select A Spider',
				'choices': [
					'Spider 1',
					'Spider 2',
				]
			},
			# second question
			{
				'type': 'list',
				'name': 'lol',
				'message': 'What to do with the Spider',
				'choices': [
					'Status',
					'Add Field',
					'Edit Field',
					'Run Now',
					'Schedule',
					'Deploy'
				]
			}
		]

		answers = prompt(questions, style=matrix_style)

		# second part question answer
		# Depending on answers run different commands
		if answers['lol'] == "Status":
			# TODO: get settings of the scrapper


			print("Current status of the selected spider")
		elif answers["lol"] == "Run Now":
			print("Call the run_scrapper script")
		elif answers["lol"] == "Add Field":
			print("Add New Field To the Scrapper")
		elif answers["lol"] == "Edit Field":
			print("Edit The field")
		elif answers["lol"] == "Schedule":
			print("Scheduled to run at ")
		elif answers["lol"] == "Deploy":
			print("Deploying to heroku")
