# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Abstract Question class (Builder pattern)"

** Separate the construction of a complex object from its representation so
that the same construction process can create different representations.

** UML LAYOUT (Builder Design Pattern)

|===================|       |=======================|
|  Director(object) |------>| AbcBuilder(interface) |
|-------------------|       |-----------------------|
| -Attribute        |       |-Attribute             |
| -Operation        |       |-Operation             |
|   +construct()    |       |   +build_part()       |
|===================|       |=======================|
                                        |
                                        |
                              |===================|
                              |  ConcreteBuilder  |
                              |-------------------|
                              |-Attribute         |
                              |-Operation         |
                              |   +build_part()   |
                              |===================|

"""
import abc


class AbcQuestions(metaclass=abc.ABCMeta):
    """
    Specify an abstract interface for creating parts of a Product
    object.
    """
    @property
    @abc.abstractmethod
    def creation_order(self):
        pass

    @property
    @abc.abstractmethod
    def _identifier(self):
        pass

    @abc.abstractmethod
    def _build_type(self):
        pass

    @abc.abstractmethod
    def _build_qmark(self):
        pass

    @abc.abstractmethod
    def _build_name(self):
        pass

    @abc.abstractmethod
    def _build_message(self):
        pass

    @abc.abstractmethod
    def _build_choices(self):
        pass

    @abc.abstractmethod
    def _build_filter(self):
        pass

    @abc.abstractmethod
    def _build_validate(self):
        pass

    @abc.abstractmethod
    def _build_default(self):
        pass


class Director(object):
    """
    Construct an object using the Builder interface.
    """

    def __init__(self):
        self._builder = None
        self._question = {}

    def construct(self, builder):
        self._question = {}
        self._builder = builder
        self._question['type'] = self._builder._build_type()
        _builder_qmark = self._builder._build_qmark()
        if _builder_qmark is not None:
            self._question['qmark'] = _builder_qmark

        self._question['name'] = self._builder._build_name()
        self._question['message'] = self._builder._build_message()
        _builder_choice = self._builder._build_choices()

        if _builder_choice is not None:
            self._question['choices'] = _builder_choice
        _builder_filter = self._builder._build_filter()
        if _builder_filter is not None:
            self._question['filter'] = _builder_filter
        _builder_validate = self._builder._build_validate()
        if _builder_validate is not None:
            self._question['validate'] = _builder_validate
        _builder_default = self._builder._build_default()
        if _builder_default is not None:
            self._question['default'] = _builder_default

    def get_question(self):
        return self._question
