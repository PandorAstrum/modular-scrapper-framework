# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Main Execution file for the Command line tools"
"""
import argparse
# from core import commands, utility
import utility

if __name__ == '__main__':
    # load all commands
    _c = utility.AutoLoader(commands, commands.AbsCommand, False)
    _choices = _c.get_names(_lower=True)
    parser = argparse.ArgumentParser()
    # arguments
    # TODO: more to add e.g: add function, stats
    parser.add_argument("operation", help="Specify an operation", choices=_choices, type=lambda s: s.lower())
    parser.add_argument("-b", help="Specify a bot")
    args = parser.parse_args()

    _invoker = commands.Invoker()
    _receiver = commands.Receiver()

    for _command in _c.loaded_module.values():
        _command = _command(_receiver)
        _invoker.store_command(_command)

    _invoker.execute_commands(args.operation)
