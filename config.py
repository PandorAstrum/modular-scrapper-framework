# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Configuration File for the tool"
"""
import os
from PyInquirer import style_from_dict, Token


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

cenegy_style = style_from_dict({
    Token.QuestionMark: '#008f11 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#008f11 bold',
    Token.Question: '#673AB7 bold',
    Token.Separator: '#6C6C6C',
})