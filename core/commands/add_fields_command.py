# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Main Exe file to Run"
"""
from .command_lines import AbsCommand
import utility


class Add(AbsCommand):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.

	"""

	@property
	def name(self):
		return 'add'

	@property
	def description(self):
		return 'Add a {field} to {this} scrapper'

	def execute(self, args):
		self._receiver.action(self, args)

	def operation(self):
		print("Adding column and field to {this} scrapper")