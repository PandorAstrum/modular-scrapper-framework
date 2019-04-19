# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Main Execution file for the Command line tools"
"""

import argparse
from core import commands
import utility

if __name__ == '__main__':
    # load all commands
    _c = utility.AutoLoader(commands, commands.AbsCommand)
    _choices = _c.get_names(_lower=True)
    _description = _c.get_names(_property_name="description")
    parser = argparse.ArgumentParser(prog='run.py', usage='%(prog)s [operation]',
                                     description="Run an Operation "
                                                 "\nUse 'python run.py <command> -h' to see each command help",
                                     formatter_class=argparse.RawTextHelpFormatter)

    # default args
    default_command = "scrapper"
    parser.add_argument("operation",
                        default=default_command,
                        const=default_command,
                        nargs="?",
                        choices=_choices,
                        type=lambda s: s.lower())

    args = parser.parse_args()
    _invoker = commands.Invoker()
    _receiver = commands.Receiver()

    for _command in _c.loaded_module.values():
        _command = _command(_receiver)
        _invoker.store_command(_command)

    _invoker.execute_commands(args.operation)