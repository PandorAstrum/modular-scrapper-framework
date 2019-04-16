# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "All question here
"""
from subprocess import Popen, PIPE
from PyInquirer import Separator
from core.questionnaire.abc_question import AbcQuestions

__all__ = [
	"SpiderSelectQuest"
]


class SpiderSelectQuest(AbcQuestions):

	@property
	def creation_order(self):
		return 1

	@property
	def _identifier(self):
		return self._build_name()

	def _build_type(self):
		return 'list'

	def _build_qmark(self):
		pass

	def _build_name(self):
		return 'spiderName'

	def _build_message(self):
		return 'Select A Spider to begin :'

	def _build_choices(self):
		_list = [Separator('==== Current Spiders ====')]
		_p = Popen(['scrapy', 'list'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		_output, _err = _p.communicate(b"stdin")
		rc = _p.returncode
		_tmp_spider_list = _output.splitlines()
		for indx, spider in enumerate(_tmp_spider_list):
			_list.append(str(indx + 1) + ". " + str(spider, 'utf-8'))
		return _list

	def _build_filter(self):
		pass

	def _build_validate(self):
		pass

	def _build_default(self):
		pass

#
#
class SecondQuest(AbcQuestions):

    @property
    def creation_order(self):
        return 2

    @property
    def _identifier(self):
        return self._build_name()

    def _build_type(self):
        return 'input'

    def _build_qmark(self):
        pass

    def _build_name(self):
        return 'bot_prefix'

    def _build_message(self):
        return 'Bot Command Prefix :'

    def _build_choices(self):
        pass

    def _build_filter(self):
        pass

    def _build_validate(self):
        pass

    def _build_default(self):
        pass
