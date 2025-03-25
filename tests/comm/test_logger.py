import pytest
import unittest

from unittest.mock import Mock

from comm import Logger, LogLevel, LOG_CARE

from tests import BaseTestCase


class LoggerTest(BaseTestCase):

    def test_logger(self):
        LOG_CARE("hello world")

        logger = Logger(self, log_level=LogLevel.INFO, log_file_name='test.log')
        logger.error("test ...")
        logger.info("this is a normal info.")
        logger.debug("this is a debug info.")

        assert True
