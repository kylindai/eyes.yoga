
import os
import re
import sys
import time
import atexit
import shutil
import asyncio
import logging
import functools

from typing import Dict, List, Union
from enum import Enum
from datetime import datetime
from logging import LogRecord

ANSI_WEAKEN = "\033[2m"
ANSI_BLACK = "\033[30m"
ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"
ANSI_YELLOW = "\033[33m"
ANSI_BLUE = "\033[34m"
ANSI_PINK = "\033[35m"
ANSI_CYAN = "\033[36m"
ANSI_WHITE = "\033[37m"
ANSI_LIGHT_BLACK = "\033[90m"
ANSI_LIGHT_RED = "\033[91m"
ANSI_LIGHT_GREEN = "\033[92m"
ANSI_LIGHT_YELLOW = "\033[93m"
ANSI_LIGHT_BLUE = "\033[94m"
ANSI_LIGHT_PINK = "\033[95m"
ANSI_LIGHT_CYAN = "\033[96m"
ANSI_LIGHT_WHITE = "\033[97m"
ANSI_REMOVE_COLOR = "\033[0m"


def LOG_PROGRESS(x):
    print(
        f"\r{ANSI_LIGHT_PINK}{x}{ANSI_REMOVE_COLOR}", end='')


def LOG_IMPORTANT(x):
    print(
        f"{ANSI_LIGHT_PINK}{x}{ANSI_REMOVE_COLOR}")


def LOG_IGNORE(x):
    print(
        f"{ANSI_WEAKEN}{x}{ANSI_REMOVE_COLOR}")


def LOG_ERROR(x):
    print(
        f"{ANSI_RED}{x}{ANSI_REMOVE_COLOR}")


def LOG_CARE(x):
    print(
        f"{ANSI_LIGHT_CYAN}{x}{ANSI_REMOVE_COLOR}")


def LOG_KV(key, value):
    print(
        f"{ANSI_YELLOW}{key} = [{ANSI_GREEN}{value}{ANSI_YELLOW}]{ANSI_REMOVE_COLOR}")


class LogLevel(Enum):
    IGNORE = ('IGR', 0)
    TRACE = ('TRC', 1)
    DEBUG = ('DBG', 2)
    INFO = ('INF', 3)
    CARE = ('CRE', 4)
    WARN = ('WRN', 5)
    ALERT = ('ALT', 6)
    ERROR = ('ERR', 7)
    FATAL = ('FTL', 8)


class LogHandler(logging.Handler):

    class Filter(logging.Filter):

        def __init__(self, log_level: LogLevel):
            super().__init__()
            self._log_level = log_level

        def do_filter(self, log_level: LogLevel):
            return log_level.value[1] < self._log_level.value[1]

        def filter(self, record):
            log_level = getattr(record, 'LogLevel')
            return self.do_filter(log_level)

    def __init__(self, name: str, log_level: LogLevel):
        super().__init__()

        self._name = name
        self._log_level = log_level

        self._filter = LogHandler.Filter(log_level)
        self.addFilter(self._filter)

    def name(self, name: str):
        self._name = name

    def log_level(self):
        return self._log_level

    def get_filter(self):
        return self._filter

    def _prompt(self) -> str:
        return f"{datetime.now()}"


class ConsoleLogHandler(LogHandler):

    class Formatter(logging.Formatter):
        def __init__(self, format: str = '%(message)s'):
            super().__init__(format)

        @staticmethod
        def do_format(name: str, log_level: LogLevel, message: str) -> str:
            color = ''
            match log_level:
                case LogLevel.IGNORE:
                    color = ANSI_WEAKEN
                case LogLevel.TRACE:
                    color = ANSI_BLUE
                case LogLevel.DEBUG:
                    color = ANSI_GREEN
                case LogLevel.INFO:
                    color = ANSI_WHITE
                case LogLevel.CARE:
                    color = ANSI_LIGHT_CYAN
                case LogLevel.WARN:
                    color = ANSI_YELLOW
                case LogLevel.ALERT:
                    color = ANSI_LIGHT_PINK
                case LogLevel.ERROR:
                    color = ANSI_RED
                case LogLevel.FATAL:
                    color = ANSI_RED
            level = log_level.value[0]
            return f"{datetime.now()}: {color}[{level}] {name}: {message}{ANSI_REMOVE_COLOR}"

        def format(self, record: LogRecord) -> Dict:
            # print(record)
            # print(record.__dict__)
            # record.__dict__[]
            name = getattr(record, 'name')
            log_level = getattr(record, 'LogLevel')
            msg = getattr(record, 'msg')
            # print("=" * 20)
            # print(f"【{msg}】")
            # print("-" * 20)
            # self._format(name, log_level, msg)
            # setattr(record, 'tm', datetime.now())
            setattr(record, 'msg',
                    ConsoleLogHandler.Formatter.do_format(name, log_level, msg))

    def __init__(self, name: str, log_level: LogLevel = LogLevel.INFO):
        super().__init__(name, log_level)
        self.setFormatter(ConsoleLogHandler.Formatter())

    def emit(self, record: LogRecord):
        self.format(record)
        # print(value['msg'])
        return super().emit(record)

    def log(self, log_level: LogLevel, message: str):
        if not self.get_filter().do_filter(log_level):
            print(ConsoleLogHandler.Formatter.do_format(
                self._name, log_level, message))


class FileLogHandler(LogHandler):

    _log_file_name = None
    _log_file = None

    _log_queue = asyncio.Queue(maxsize=100)

    def __init__(self, name: str, log_level: LogLevel = LogLevel.IGNORE):
        super().__init__(name, log_level)
        atexit.register(self._clearup)

    def _clearup(self):
        """ close log file """
        if FileLogHandler._log_file is not None:
            FileLogHandler._log_file.close()
            FileLogHandler._back_log_file()

    @staticmethod
    async def _submit_log(log_message: str):
        await FileLogHandler._log_queue.put(log_message)

    @staticmethod
    async def _write_log():
        while True:
            print("wait log message")
            log_message = await FileLogHandler._log_queue.get()
            print("got log message", log_message)
            if FileLogHandler._log_file is not None:
                try:
                    FileLogHandler._log_file.write(log_message)
                    FileLogHandler._log_file.flush()
                except Exception as e:
                    # print(e)
                    pass
            FileLogHandler._log_queue.task_done()

    @staticmethod
    def set_log_file_name(file_name: str = None):
        log_path = os.path.abspath("./log")
        if not os.path.exists(log_path):
            os.makedirs(log_path, exist_ok=True)
        if file_name is None:
            file_name = f"{os.path.splitext(sys.argv[0])[0]}.log"
        FileLogHandler._log_file_name = os.path.join(log_path, file_name)
        try:
            FileLogHandler._log_file = open(
                FileLogHandler._log_file_name, "w+")
            # asyncio.create_task(FileLogHandler._write_log())
        except Exception as e:
            print(e)

    @staticmethod
    def _back_log_file():
        if not FileLogHandler._log_file_name:
            return
        file_old = os.path.join(FileLogHandler._log_file_name)
        if not os.path.exists(file_old):
            return
        # log bak path
        log_path = os.path.dirname(FileLogHandler._log_file_name)
        file_name = os.path.basename(FileLogHandler._log_file_name)
        log_bak_path = os.path.join(log_path, "bak")
        if not os.path.exists(log_bak_path):
            os.makedirs(log_bak_path, exist_ok=True)
        # log bak file name
        file_prefix = os.path.splitext(file_name)[0]
        file_date = datetime.now().strftime('%Y%m%d')
        file_seq = 0
        # find file seq
        file_list = os.listdir(log_bak_path)
        if file_list:
            file_pattern = re.compile(f"{file_prefix}-{file_date}-(\\d+).log")
            for file in file_list:
                if file_pattern.search(file):
                    seq = int(file_pattern.search(file).group(1))
                    file_seq = max(file_seq, seq)
        file_bak = os.path.join(
            log_bak_path, f"{file_prefix}-{file_date}-{file_seq+1}.log")
        shutil.move(file_old, file_bak)

    def emit(self, record: LogRecord) -> None:
        return super().emit(record)

    def log(self, log_level: LogLevel, message: str):
        if not self.get_filter().do_filter(log_level):
            if FileLogHandler._log_file is not None:
                try:
                    level = log_level.value[0]
                    log_message = f"{self._prompt()}: [{level}] {self._name}: {message}\n"
                    # asyncio.create_task(FileLogHandler._submit_log(log_message))
                    FileLogHandler._log_file.write(log_message)
                    FileLogHandler._log_file.flush()
                except Exception as e:
                    # print(e)
                    pass


class Logger:

    Level = LogLevel
    _log_level = LogLevel.INFO

    def __init__(self,
                 name: Union[str, object],
                 sub_name: str = None,
                 trace: bool = True,
                 log_level: LogLevel = None):
        if isinstance(name, str):
            self._name = name
        else:
            self._name = name.__class__.__name__

        if sub_name is not None:
            self._name = self._name + '.' + sub_name

        if log_level is not None:
            Logger._log_level = log_level
        self._log_level = Logger._log_level

        self._trace = trace

        self._handlers = {
            'console': ConsoleLogHandler(self._name, self._log_level),
            'file': FileLogHandler(self._name)
        }

        self._logger = logging.getLogger(self._name)
        self._logger.setLevel(logging.INFO)
        if not self._logger.handlers:
            self._logger.addHandler(self._handlers['console'])
            self._logger.addHandler(self._handlers['file'])

        if self._trace:
            self._start = time.time()
            self._log(LogLevel.TRACE, '<<<')

    def __del__(self):
        if self._trace:
            cost = (time.time() - self._start) * 1000.0
            trace_left = '>>>'
            if cost < 1000:
                trace_left = f'>>> cost: {cost:.3f}ms'
            elif cost < 60000:
                trace_left = f'>>> cost: {(cost/1000.0):.3f}s'
            elif cost < 3600000:
                trace_left = f'>>> cost: {(cost/60000.0):.3f}m'
            else:
                trace_left = f'>>> cost: {(cost/3600000.0):.3f}h'
            self._log(LogLevel.TRACE, trace_left)

    def _log(self, log_level: LogLevel, message: str):
        # self._logger.info(message, extra={'LogLevel': log_level})
        for _, handler in self._handlers.items():
            handler.log(log_level, message)

    def set_log_file_name(self, file_name: str):
        FileLogHandler.set_log_file_name(file_name)
        return self

    def name(self):
        return self._name

    def ignore(self, message: str):
        self._log(LogLevel.IGNORE, message)

    def trace(self, message: str):
        self._log(LogLevel.TRACE, message)

    def debug(self, message: str):
        self._log(LogLevel.DEBUG, message)

    def info(self, message: str):
        self._log(LogLevel.INFO, message)

    def care(self, message: str):
        self._log(LogLevel.CARE, message)

    def warn(self, message: str):
        self._log(LogLevel.WARN, message)

    def alert(self, message: str):
        self._log(LogLevel.ALERT, message)

    def error(self, message: str):
        self._log(LogLevel.ERROR, message)

    def fatal(self, message: str):
        self._log(LogLevel.FATAL, message)
