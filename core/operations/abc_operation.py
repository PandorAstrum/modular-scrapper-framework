# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "Description of this file here"
"""
import abc


class OperationExecutioner(object):
    """
    Ask the command to carry out the request.
    """

    def __init__(self):
        self._operations = []

    def store_operation(self, operation):
        self._operations.append(operation)

    def execute_operation(self, operation_name, settings_file, selected_spider_name):
        for operation in self._operations:
            operation.execute(operation_name, settings_file, selected_spider_name)


class OperationReceiver(object):
    """
    Know how to perform the operations associated with carrying out a
    request. Any class may serve as a Receiver.
    """
    def action(self, cls, operation_name, settings_file, selected_spider_name):
        if cls._identifier == operation_name:
            cls.operation(settings_file, selected_spider_name)


class AbsOperation(metaclass=abc.ABCMeta):
    """
    Declare an interface for executing an operation.
    """

    def __init__(self, receiver):
        self._operation_receiver = receiver

    @property
    @abc.abstractmethod
    def creation_order(self):
        pass

    @property
    @abc.abstractmethod
    def _identifier(self):
        pass

    @abc.abstractmethod
    def execute(self, operation_name, settings_file, selected_spider_name):
        pass

    @abc.abstractmethod
    def operation(self, settings_file, selected_spider_name):
        pass
