# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Main Exe file to Run"
"""
import sys
from subprocess import Popen, PIPE
from .command_lines import AbsCommand


class List(AbsCommand):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This class is responsible to scan the general spiders folder for all scrappers **
	"""

	@property
	def name(self):
		return 'list'

	@property
	def description(self):
		return 'List all the Scrappers in the framework'

	def execute(self, args):
		self._receiver.action(self, args)

	def operation(self):
		if len(sys.argv) > 3:
			print("help asked")
		else:
			p = Popen(['scrapy', 'list'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
			output, err = p.communicate(b"stdin")
			rc = p.returncode
			tmp_spider_list = output.splitlines()
			for indx, t in enumerate(tmp_spider_list):
				print(str(indx+1) + ". " + str(t, 'utf-8'))
		# fancy styled cmd here

