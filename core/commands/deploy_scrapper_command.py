# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Main Exe file to Run"
"""
from .command_lines import AbsCommand
import utility


class Deploy(AbsCommand):
	"""
	Define a binding between a Receiver object and an action.
	Implement Execute by invoking the corresponding operation(s) on
	Receiver.

	"""

	@property
	def name(self):
		return 'deploy'

	@property
	def description(self):
		return 'deploy {this} scrapper into {crawlera}'

	def execute(self, args):
		self._receiver.action(self, args)

	def operation(self):
		print("deploying {this} scrapper into {crawlera}")
