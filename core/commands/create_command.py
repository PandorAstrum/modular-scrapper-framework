# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Main Exe file to Run"
"""
import utility
from .command_lines import AbsCommand
from PyInquirer import prompt
from config import matrix_style
# from core import utility, projects
# from core.questions.abc_question import Director
# from core.projects.abc_projects import AbsProject, Project
# from core.questions.create_what import CreateQuestion


class Create(AbsCommand):
    """
    Define a binding between a Receiver object and an action.
    Implement Execute by invoking the corresponding operation(s) on
    Receiver.
    """

    @property
    def name(self):
        return 'create'

    @property
    def description(self):
        return 'Create the JSON Settings for spider'

    def execute(self, args):
        self._receiver.action(self, args)

    def operation(self):
        _director = Director()
        # first question what to create
        _project_class = utility.AutoLoader(projects, AbsProject, True)
        _project_names = _project_class.get_names()

        _director.construct(CreateQuestion(_project_names))
        _question = [_director.get_question()]
        _answer = prompt(_question, style=matrix_style)

        for _p in _project_class.get_names(_lower=True):
            if _p == _answer["create_what"]:
                _initialize_project = _project_class.initialize(_p)
                _project = Project(_initialize_project)
                _project.project_interface()

        #                  Separator('= Bot Commands ='),
        #                  {'name': 'help', 'checked': True},
        #                  {'name': 'logout', 'checked': True},
        #                  {'name': 'join'},
        #                  {'name': 'leave'},
        #                  {'name': 'clear'},
        #                  {'name': 'displayEmbed'},
        #                  {'name': 'play'},
        #                  {'name': 'pause'},
        #                  {'name': 'stop'},
        #                  {'name': 'resume'},
        #                  {'name': 'queue'},
        #                  Separator('= Custom Command ='),
        #                  {'name': 'hug'},
        #                  {'name': 'roll'},
        #                  Separator('= The extras ='),
        #                  {'name': 'Pineapple'}
        #              ],
        #              'validate': lambda answer: 'You must choose at least one events or commands.' if len(answer) == 0 else True
        #              },
        #             # discord invite
        #             {'type': 'input',
        #              'name': 'bot_channel',
        #              'message': 'Discord Channel :', },
        #             # discord token
        #             {'type': 'input',
        #              'name': 'bot_token',
        #              'message': 'Token :', },
        #             # user.json
        #             {'type': 'confirm',
        #              'message': 'Do you want to generate USER file?',
        #              'name': 'user_file',
        #              'default': True},
        #             # API integration
        #             {'type': 'checkbox',
        #              'qmark': '😃',
        #              'message': 'Select API to add :',
        #              'name': 'bot_api',
        #              'choices': [
        #                  Separator('= APIs ='),
        #                  {'name': 'Leauge of legends'},
        #                  {'name': 'PUBG'}
        #              ]
        #              },
        #     ]

        #     # add functionality
        #     {'type': 'checkbox',
        #      'qmark': '😃',
        #      'message': 'Select functions to add :',
        #      'name': 'bot_func',
        #      'choices': [
        #          Separator('= Bot Events ='),
        #          {'name': 'on_ready', 'checked': True},
        #          {'name': 'on_resumed'},
        #          {'name': 'on_error'},
        #          {'name': 'on_message', 'checked': True},
        #          {'name': 'on_massage_edit'},
        #          {'name': 'on_massage_delete'},
        #          {'name': 'on_reaction_add'},
        #          {'name': 'on_reaction_clear'},
        #          {'name': 'on_reaction_remove'},
        #          {'name': 'on_channel_create'},
        #          {'name': 'on_channel_update'},
        #          {'name': 'on_channel_delete'},
        #          {'name': 'on_member_join'},
        #          {'name': 'on_member_update'},
        #          {'name': 'on_member_remove'},
        #          {'name': 'on_server_join'},
        #          {'name': 'on_server_update'},
        #          {'name': 'on_server_remove'},
        #          {'name': 'on_server_role_create'},
        #          {'name': 'on_server_role_update'},
        #          {'name': 'on_server_role_delete'},
        #          {'name': 'on_server_available'},
        #          {'name': 'on_server_unavailable'},
        #          {'name': 'on_server_emoji_update'},
        #          Separator('= Bot Commands ='),
        #          {'name': 'help', 'checked': True},
        #          {'name': 'logout', 'checked': True},
        #          {'name': 'join'},
        #          {'name': 'leave'},
        #          {'name': 'clear'},
        #          {'name': 'displayEmbed'},
        #          {'name': 'play'},
        #          {'name': 'pause'},
        #          {'name': 'stop'},
        #          {'name': 'resume'},
        #          {'name': 'queue'},
        #          Separator('= Custom Command ='),
        #          {'name': 'hug'},
        #          {'name': 'roll'},
        #          Separator('= The extras ='),
        #          {'name': 'Pineapple'}
        #      ],
        #      'validate': lambda answer: 'You must choose at least one events or commands.' if len(answer) == 0 else True
        #      },
        #     # discord invite
        #     {'type': 'input',
        #      'name': 'bot_channel',
        #      'message': 'Discord Channel :', },
        #     # discord token
        #     {'type': 'input',
        #      'name': 'bot_token',
        #      'message': 'Token :', },
        #     # user.json
        #     {'type': 'confirm',
        #      'message': 'Do you want to generate USER file?',
        #      'name': 'user_file',
        #      'default': True},
        #     # API integration
        #     {'type': 'checkbox',
        #      'qmark': '😃',
        #      'message': 'Select API to add :',
        #      'name': 'bot_api',
        #      'choices': [
        #          Separator('= APIs ='),
        #          {'name': 'Leauge of legends'},
        #          {'name': 'PUBG'}
        #      ]
        #      },
        #     # confirm
        #     {'type': 'confirm',
        #      'message': 'Do you want to continue?',
        #      'name': 'continue',
        #      'default': True}
        # ]
        # _answers = prompt(questions, style=matrix_style)
        # while _answers['continue'] == "No":
        #     pass

        # {
        #     "bot": [{
        #         "func": {
        #             "func1": {
        #                 "id": 2,
        #                 "type": "command",
        #                 "desc": "First function",
        #                 "usage": "command channel",
        #                 "help": "help command"
        #             },
        #             "func2": {
        #                 "id": 3,
        #                 "type": "func",
        #                 "desc": "Some text",
        #                 "usage": "command channel",
        #                 "help": "help command"
        #             }
        #         },
        #         "discord": {
        #             "channel": "value",
        #             "username": "value",
        #             "password": "value"
        #         }
        #     }]
        # }