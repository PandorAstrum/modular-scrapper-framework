# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Main Exe file to Run"
"""
from .command_lines import AbsCommand
import utility


class Schedule(AbsCommand):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.

	"""

	@property
	def name(self):
		return 'schedule'

	@property
	def description(self):
		return 'Schedule a scrapper to run in a time frame'

	def execute(self, args):
		self._receiver.action(self, args)

	def operation(self):
		print("Your {this} scrapper is scheduled to run in every {14} days")
