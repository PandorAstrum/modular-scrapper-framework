# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Command Design Pattern"

** Encapsulate a request as an object, thereby letting you parameterize
clients with different requests, queue or log requests, and support
undoable operations.

** UML LAYOUT (Command Design Pattern)

|===================|       |=======================|       |===========================|
|   Client(object)  |       |    Invoker(object)    |------>|   AbsCommand(interface)   |
|      *main()      |       |-----------------------|       |---------------------------|
|-------------------|       | -Attribute            |       | -Attribute                |
| -Attribute        |       | -Operation            |       | -Operation                |
| -Operation        |       |   +store_commands()   |       |   +execute()              |
|===================|       |   +execute_command()  |       |   +undo()                 |
    |       |               |=======================|       |===========================|
    |       |                                                           |
    |       |                                                           |
    |       |               |======================|          |=======================|
    |       |-------------->|   Receiver(object)   |<---------|    ConcreteCommand    |
    |                       |----------------------|          |-----------------------|
    |                       | -Attribute           |          | -Attribute            |
    |                       | -Operation           |          | -Operation            |
    |                       |   +action()          |          |   +execute()          |
    |                       |======================|          |   +undo()             |
    |-------------------------------------------------------->|=======================|

"""
import abc


class Invoker(object):
    """
    Ask the command to carry out the request.
    """

    def __init__(self):
        self._commands = []

    def store_command(self, command):
        self._commands.append(command)

    def execute_commands(self, args):
        for command in self._commands:
            command.execute(args)


class Receiver(object):
    """
    Know how to perform the operations associated with carrying out a
    request. Any class may serve as a Receiver.
    """

    def action(self, cls, args):
        if cls.name == args:
            cls.operation()


class AbsCommand(metaclass=abc.ABCMeta):
    """
    Declare an interface for executing an operation.
    """

    def __init__(self, receiver):
        self._receiver = receiver

    @property
    @abc.abstractmethod
    def name(self):
        pass

    @property
    @abc.abstractmethod
    def description(self):
        pass

    @abc.abstractmethod
    def execute(self, args):
        pass

    @abc.abstractmethod
    def operation(self):
        pass
