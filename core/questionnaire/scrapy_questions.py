# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Description of this file here"
"""

# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Main Exe file to Run"
"""
from PyInquirer import Separator
from core.questionnaire.abc_question import AbcQuestions
import utility
# from core import utility, structures
# from core.templates import discord_events, discord_commands
# from core.templates.abc_template import AbcTemplate


class SpiderSelectQuest(AbcQuestions):

	@property
	def creation_order(self):
		return 1

	@property
	def _identifier(self):
		return self._build_name()

	def _build_type(self):
		return 'checkbox'

	def _build_qmark(self):
		return '😃'

	def _build_name(self):
		return 'bot_events'

	def _build_message(self):
		return 'Select Events for the bot :'

	def _build_choices(self):
		_list = [Separator('==== Bot Events ====')]
		# _t = utility.AutoLoader(discord_events, AbcTemplate, True)
		# _t_initialized = _t.initialize_each()
		_t_initialized = ["abracadabra", "dubai get on"]
		for i in _t_initialized:
			_list.append(i)
		return _list

	def _build_filter(self):
		pass

	def _build_validate(self):
		return lambda answer: 'You must choose at least one Events.' if len(answer) == 0 else True

	def _build_default(self):
		pass

#
#
# class BotPrefixQuestion(AbcQuestions):
#
#     @property
#     def creation_order(self):
#         return 2
#
#     @property
#     def _identifier(self):
#         return self._build_name()
#
#     def _build_type(self):
#         return 'input'
#
#     def _build_qmark(self):
#         pass
#
#     def _build_name(self):
#         return 'bot_prefix'
#
#     def _build_message(self):
#         return 'Bot Command Prefix :'
#
#     def _build_choices(self):
#         pass
#
#     def _build_filter(self):
#         pass
#
#     def _build_validate(self):
#         pass
#
#     def _build_default(self):
#         pass
#
#
# class BotStructureQuestion(AbcQuestions):
#
#     @property
#     def creation_order(self):
#         return 3
#
#     @property
#     def _identifier(self):
#         return self._build_name()
#
#     def _build_type(self):
#         return 'list'
#
#     def _build_qmark(self):
#         pass
#
#     def _build_name(self):
#         return 'bot_structure'
#
#     def _build_message(self):
#         return 'Bot Folder Structure :'
#
#     def _build_choices(self):
#         _get_platform_specific_structure = utility.AutoLoader(structures.discord_structure, structures.AbcDiscordStructure, True)
#         return _get_platform_specific_structure.get_names()
#
#     def _build_filter(self):
#         return lambda val: val.lower()
#
#     def _build_validate(self):
#         pass
#
#     def _build_default(self):
#         pass
#
#
# class BotEventQuestion(AbcQuestions):
#
#     @property
#     def creation_order(self):
#         return 4
#
#     @property
#     def _identifier(self):
#         return self._build_name()
#
#     def _build_type(self):
#         return 'checkbox'
#
#     def _build_qmark(self):
#         return '😃'
#
#     def _build_name(self):
#         return 'bot_events'
#
#     def _build_message(self):
#         return 'Select Events for the bot :'
#
#     def _build_choices(self):
#         _list = [Separator('==== Bot Events ====')]
#         _t = utility.AutoLoader(discord_events, AbcTemplate, True)
#         _t_initialized = _t.initialize_each()
#         for i in _t_initialized:
#             _list.append(i.get_object())
#         return _list
#
#     def _build_filter(self):
#         pass
#
#     def _build_validate(self):
#         return lambda answer: 'You must choose at least one Events.' if len(answer) == 0 else True
#
#     def _build_default(self):
#         pass
#
#
# class BotCommandQuestion(AbcQuestions):
#
#     @property
#     def creation_order(self):
#         return 5
#
#     @property
#     def _identifier(self):
#         return self._build_name()
#
#     def _build_type(self):
#         return 'checkbox'
#
#     def _build_qmark(self):
#         return '😃'
#
#     def _build_name(self):
#         return 'bot_commands'
#
#     def _build_message(self):
#         return 'Select Commands for the bot :'
#
#     def _build_choices(self):
#         _list = [Separator('==== Bot Commands ====')]
#         _t = utility.AutoLoader(discord_commands, AbcTemplate, True)
#         _t_initialized = _t.initialize_each()
#         for i in _t_initialized:
#             _list.append(i.get_object())
#         return _list
#
#     def _build_filter(self):
#         pass
#
#     def _build_validate(self):
#         return lambda answer: 'You must choose at least one Commands.' if len(answer) == 0 else True
#
#     def _build_default(self):
#         pass
#
#
# class BotUserQuestion(AbcQuestions):
#
#     @property
#     def creation_order(self):
#         return 7
#
#     @property
#     def _identifier(self):
#         return self._build_name()
#
#     def _build_type(self):
#         return 'confirm'
#
#     def _build_qmark(self):
#         pass
#
#     def _build_name(self):
#         return 'bot_user'
#
#     def _build_message(self):
#         return 'Do you want to generate USER Json file?'
#
#     def _build_choices(self):
#         pass
#
#     def _build_filter(self):
#         pass
#
#     def _build_validate(self):
#         pass
#
#     def _build_default(self):
#         return True
#
#
# class BotSystemQuestion(AbcQuestions):
#
#     @property
#     def creation_order(self):
#         return 8
#
#     @property
#     def _identifier(self):
#         return self._build_name()
#
#     def _build_type(self):
#         return 'input'
#
#     def _build_qmark(self):
#         pass
#
#     def _build_name(self):
#         return 'bot_system'
#
#     def _build_message(self):
#         return 'Choose a System to add :'
#
#     def _build_choices(self):
#         pass
#
#     def _build_filter(self):
#         pass
#
#     def _build_validate(self):
#         pass
#
#     def _build_default(self):
#         pass
#
#
# class BotAPIQuestion(AbcQuestions):
#
#     @property
#     def creation_order(self):
#         return 9
#
#     @property
#     def _identifier(self):
#         return self._build_name()
#
#     def _build_type(self):
#         return 'input'
#
#     def _build_qmark(self):
#         pass
#
#     def _build_name(self):
#         return 'bot_api'
#
#     def _build_message(self):
#         return 'Choose any API to add :'
#
#     def _build_choices(self):
#         pass
#
#     def _build_filter(self):
#         pass
#
#     def _build_validate(self):
#         pass
#
#     def _build_default(self):
#         pass
