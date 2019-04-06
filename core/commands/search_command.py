# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Main Exe file to Run"
"""
from .command_lines import AbsCommand
from core import utility

class Search(AbsCommand):
    """
    Define a binding between a Receiver object and an action.
    Implement Execute by invoking the corresponding operation(s) on
    Receiver.
    """

    @property
    def name(self):
        return 'search'

    @property
    def description(self):
        return 'Search the bot folder for bots'

    def execute(self, args):
        self._receiver.action(self, args)

    def operation(self):
        # _bot_files = utility.search_file(BOT_FOLDER, "*_bot.json", "files")
        _tmp = []
        # for _bot in _bot_files:
        #     _tmp.append(_bot.replace('_bot.json', ''))
        print(_tmp)
