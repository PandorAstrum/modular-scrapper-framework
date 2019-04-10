# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Main Exe file to Run"
"""
from .command_lines import AbsCommand
import sys


class Run(AbsCommand):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.
	** This class is responsible to run a scrapper based on a json settings
	"""

	@property
	def name(self):
		return 'run'

	@property
	def description(self):
		return 'run {this} scrapper'

	def execute(self, args):
		self._receiver.action(self, args)

	def operation(self):
		# TODO: show all the available spiders
		# get the list of scrapper and put it

		# run questions which one to run
		# select numbers
		# according to numbers run the spiders
		if len(sys.argv) < 3:
			print("No scrapper Specified")
		else:
			pass
		# TODO: ask for any edit or add
		# TODO: deploy or schedule to run or run now

		print("running {this} scrapper")
