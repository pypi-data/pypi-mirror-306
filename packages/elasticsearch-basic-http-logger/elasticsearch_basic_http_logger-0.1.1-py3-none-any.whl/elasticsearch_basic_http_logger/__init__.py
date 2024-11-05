import base64
import dataclasses
import logging
import os
import sys
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from logging import LogRecord
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

REQUEST_MAX_POOL_SIZE = 100

__version__ = '0.1.1'


def get_thread_id():
    return threading.get_ident()


@dataclasses.dataclass
class ESLoggerConfig:
    url: str
    index_prefix: str
    app_name: str
    app_version: str = ""
    formatter: Optional[str] = None
    username: Optional[str] = None
    passwd: Optional[str] = None
    level: int = logging.NOTSET
    silent: bool = True
    http_thread_workers: int = 8

    def as_logging_handler_dict(self, formatter: Optional[str] = None):
        _formatter = None
        if formatter:
            _formatter = formatter
        elif self.formatter:
            _formatter = self.formatter

        config_dict = {
            'class': 'elasticsearch_basic_http_logger.DongDongESLogger',
            'level': self.level,
            'app_name': self.app_name,
            'app_version': self.app_version,
            'url': self.url,
            'index_prefix': self.index_prefix,
            'username': self.username,
            'passwd': self.passwd,
            'silent': self.silent,
            'http_thread_workers': self.http_thread_workers,
        }

        if _formatter:
            config_dict['formatter'] = _formatter

        return config_dict


def get_user_password_base64(username, password):
    return base64.b64encode(f'{username}:{password}'.encode('ascii')).decode('ascii')


class DongDongESLogger(logging.Handler):
    def __init__(self, url, index_prefix, app_name,
                 app_version="",
                 username: Optional[str] = None,
                 passwd: Optional[str] = None,
                 formatter: Optional[str] = None,
                 level=logging.NOTSET,
                 silent: bool = True,
                 http_thread_workers=8):
        super().__init__(level)
        self.silent = silent
        self.formatter = formatter

        if not self.silent:
            print(
                f'[thread:{get_thread_id()}]elasticsearch_basic_http_logger: ' +
                f'url={url}, index_prefix={index_prefix}, username={username}, len(passwd)={len(passwd)}, ' +
                f'level={level}, silent={silent}, http_thread_workers={http_thread_workers}',
            )

        self.url = url
        self.index_prefix = index_prefix
        self.app_name = app_name
        self.app_version = app_version
        self.executor = ThreadPoolExecutor(max_workers=http_thread_workers)

        if username and passwd:
            self.auth_headers = {
                'Authorization': 'Basic ' + get_user_password_base64(username=username, password=passwd)
            }
        else:
            self.auth_headers = dict()

        self.session = requests.Session()

        # noinspection HttpUrlsUsage
        for prefix in ['http://', 'https://']:
            self.session.mount(prefix, HTTPAdapter(
                max_retries=Retry(
                    total=5,
                    backoff_factor=0.5,
                    status_forcelist=[403, 500, 503]
                ),
                pool_connections=REQUEST_MAX_POOL_SIZE,
                pool_maxsize=REQUEST_MAX_POOL_SIZE,
            ))

    def emit(self, record: LogRecord):
        self.executor.submit(self._emit, record)

    @property
    def index(self):
        dt_str = datetime.now().strftime('%Y-%m-%d')
        return f"{self.index_prefix}-{dt_str}"

    def _emit(self, record):
        try:
            data = {
                'level': record.levelname,
                'app_name': self.app_name,
                'app_version': self.app_version,
                'message': self.format(record),
                'log_time': int(1000 * time.time())
            }
            if hasattr(record, 'action'):
                data['action'] = record.action
            if hasattr(record, 'digest'):
                data['digest'] = record.digest
            url = os.path.join(self.url, self.index + '/_doc')
            resp = requests.post(url, json=data, timeout=3.0, headers=self.auth_headers)
            if not self.silent:
                print(
                    f'[thread:{get_thread_id()}]elasticsearch_basic_http_logger: url={url}, ' +
                    f'headers={self.auth_headers}, data={data}, resp={resp.text}'
                )

        except Exception as e:
            print(f'[thread:{get_thread_id()}]elasticsearch_basic_http_logger: {e}', file=sys.stderr)
