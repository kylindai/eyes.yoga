import asyncio
import pytest
import unittest

from comm import Logger, LOG_KV, LOG_IMPORTANT, LOG_CARE, LOG_IGNORE


class AsyncTestCase(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setup_class(cls):
        LOG_CARE(f"\nTestCase: {cls.__name__} <<<")

    @classmethod
    def teardown_class(cls):
        LOG_CARE(f"TestCase: {cls.__name__} >>>")

    async def asyncSetup(self):
        # MysqlClient(test_mode=True)
        # open resource by asyncio
        pass

    async def asyncTearDown(self):
        # await MysqlClient().shutdown()
        # await close resource by asyncio
        pass

    def setup_method(self, method):
        LOG_IGNORE(f"before method: {method.__name__}")

    def teardown_method(self, method):
        LOG_IGNORE(f"after method: {method.__name__}")
