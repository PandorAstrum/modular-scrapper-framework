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
    _c = utility.AutoLoader(commands, commands.AbsCommand, False)
    _choices = _c.get_names(_lower=True)
    _description = _c.get_names(_property_name="description")
    parser = argparse.ArgumentParser(prog='run.py', usage='%(prog)s [operations]',
                                     description="Run an Operation "
                                                 "\nUse 'python run.py <command> -h' to see each command help",
                                     formatter_class=argparse.RawTextHelpFormatter)
    # arguments
    # TODO: more to add e.g: add function, stats

    parser.add_argument("operation", choices=_choices, nargs="+", type=lambda s: s.lower())


    # blame.add_argument(
    #     '--dry-run',
    #     help='do not blame, just pretend',
    #     action='store_true'
    # )
    # for indx, c in enumerate(_choices):
    #     parser.add_argument(c, metavar=c, nargs='+', help=_description[indx])

    args = parser.parse_args()

    _invoker = commands.Invoker()
    _receiver = commands.Receiver()

    for _command in _c.loaded_module.values():
        _command = _command(_receiver)
        _invoker.store_command(_command)

    _invoker.execute_commands(args.operation)
