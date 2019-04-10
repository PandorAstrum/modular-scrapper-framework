# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Main Exe file to Run"
"""
from .command_lines import AbsCommand
import utility


class Run(AbsCommand):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.

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
		print("running {this} scrapper")