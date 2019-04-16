# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Main Exe file to Run"
"""
import sys
from subprocess import Popen, PIPE

from .command_lines import AbsCommand
import utility
from PyInquirer import prompt
from config import matrix_style
# from core import utility, projects
from core.questionnaire.abc_question import Director
from core.questionnaire.scrapy_questions import SpiderSelectQuest


class Initializer(AbsCommand):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.

	"""

	@property
	def name(self):
		return 'Initialize'

	@property
	def description(self):
		return 'Initialize the CLI'

	def execute(self, args):
		self._receiver.action(self, args)

	def operation(self):
		_director = Director()
		# first question select a spider
		if len(sys.argv) > 3:
			print("help asked")
		else:
			p = Popen(['scrapy', 'list'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
			output, err = p.communicate(b"stdin")
			rc = p.returncode
			tmp_spider_list = output.splitlines()
			for indx, t in enumerate(tmp_spider_list):
				print(str(indx+1) + ". " + str(t, 'utf-8'))

		# _project_class = utility.AutoLoader(projects, AbsProject, True)
		# _project_names = _project_class.get_names()

		# _director.construct(SpiderSelectQuest())
		# _question = [_director.get_question()]
		# _answer = prompt(_question, style=matrix_style)

		# for _p in _project_class.get_names(_lower=True):
		# 	if _p == _answer["create_what"]:
		# 		_initialize_project = _project_class.initialize(_p)
		# 		_project = Project(_initialize_project)
		# 		_project.project_interface()
