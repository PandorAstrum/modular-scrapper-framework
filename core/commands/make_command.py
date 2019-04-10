# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Main Exe file to Run"
"""
import sys
import utility
from utility import readJSON
from .command_lines import AbsCommand


class Make(AbsCommand):
    """
    Define a binding between a Receiver object and an action.
    Implement Execute by invoking the corresponding operation(s) on
    Receiver.
    """

    @property
    def name(self):
        return 'make'

    @property
    def description(self):
        return 'Generate the spider from JSON settings'

    def execute(self, args):
        self._receiver.action(self, args)

    def operation(self):
        # get extra arguments from command lines
        if len(sys.argv) < 3:
            print("No Bot Specified")
        else:
            pass
        # get bot name
        #     _bot_arg_parse = sys.argv[3]
        #     _bot_name = _bot_arg_parse + "_bot.json"
        #     _file = utility.search_file(BOT_FOLDER, _bot_name, "path")
        #     if _file:
        #         _bot = readJSON(_file[0])
        #         _bot_object = _bot['bot']
        #
        #         # _bot_type = _bot_object['basic']['type']
        #         self.create_bot(_bot_object)
        #     else:
        #         print(f"No bot found named {_bot_arg_parse}")

    def create_bot(self, _bot_object):
        _bot_platform = _bot_object['platform']
        _bot_basic = _bot_object['basic']
        _bot_structure = _bot_basic['type']
        # depending on platform load modules
        from core import platform
        _platform = utility.AutoLoader(platform, platform.AbcPlatform)
        for _p in _platform.get_names(_lower=True):
            if _p == _bot_platform:
                s = _platform.initialize(_p)
                s.build_bot(_bot_object)