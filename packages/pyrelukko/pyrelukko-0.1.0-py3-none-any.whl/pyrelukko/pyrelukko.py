"""
TBD
"""
import asyncio
import logging
import os
import json
import threading
import ssl
import time

from datetime import datetime
from typing import Dict, List, Union
from pathlib import Path
from urllib3.util import Url, parse_url
from urllib3.util.retry import Retry

import requests
from websockets import ConnectionClosed as WsConnectionClosed

from websockets.asyncio.client import connect as ws_connect

from .retry import retry

SSL_KWARGS = [
    'check_hostname',
    'hostname_checks_common_name',
    'verify_mode',
    'verify_flags',
    'options',
]

logger = logging.getLogger(__name__)


class RelukkoDoRetry(Exception):
    """
    Exception thrown on some errors which we still want to retry
    """

# pylint: disable=too-many-instance-attributes
class RelukkoClient:
    """
    TBD
    """
    def __init__(
            self, base_url: Union[Url, str], api_key:str, **kwargs) -> None:
        """
        TBD
        """
        self.session = requests.Session()
        self.api_key = api_key
        self._setup_session(api_key, **kwargs)
        self._setup_http_adapters_retry(**kwargs)

        self.base_url = self._setup_base_url(base_url)
        self.ws_url = self._setup_ws_url(str(self.base_url))
        self.ssl_ctx = None
        self._setup_ssl_ctx(**kwargs)

        # event for websocket thread to signal it got a message
        self.message_received = threading.Event()
        # As long as it's set the websocket thread runs
        self.ws_running = threading.Event()
        self.ws_listener: threading.Thread = None

    def reconfigure_relukko(
            self, base_url: Union[Url, str]=None, api_key: str=None, **kwargs):
        """
        TBD
        """
        self.api_key = api_key or self.api_key
        self._setup_session(self.api_key, **kwargs)
        self._setup_http_adapters_retry(**kwargs)
        self.base_url = self._setup_base_url(base_url or self.base_url)
        self.ws_url = self._setup_ws_url(str(self.base_url))
        self._setup_ssl_ctx(**kwargs)

    def _setup_http_adapters_retry(self, **kwargs):
        for _, http_adapter in self.session.adapters.items():
            http_retry: Retry = http_adapter.max_retries
            for key, value in kwargs.items():
                if hasattr(http_retry, key):
                    setattr(http_retry, key, value)
            http_adapter.max_retries = http_retry

    def _setup_session(self, api_key: str, **kwargs):
        self.session.headers = {'X-api-Key': api_key}
        for key, value in kwargs.items():
            if hasattr(self.session, key):
                setattr(self.session, key, value)

    def _setup_ssl_ctx(self, **kwargs) -> Union[ssl.SSLContext, None]:
        if self.ws_url.scheme == "wss":
            if self.ssl_ctx is None:
                self.ssl_ctx = ssl.create_default_context(
                    ssl.Purpose.SERVER_AUTH)
            for kwarg in SSL_KWARGS:
                setattr(
                    self.ssl_ctx,
                    kwarg,
                    kwargs.get(kwarg, getattr(self.ssl_ctx, kwarg)))

            # Try to behave like requests library and take *_CA_BUNDLE env vars
            # into account.
            ca_bundle = (
                os.environ.get("REQUESTS_CA_BUNDLE")
                or os.environ.get("CURL_CA_BUNDLE"))

            ca_bundle_file = None
            ca_bundle_path = None
            if ca_bundle is not None:
                ca_bundle = Path(ca_bundle)
                ca_bundle_file = ca_bundle if ca_bundle.is_file() else None
                ca_bundle_path = ca_bundle if ca_bundle.is_dir() else None

            # values from kwargs take precedence env vars
            ca_file = kwargs.get('cafile', ca_bundle_file)
            ca_path = kwargs.get('capath', ca_bundle_path)
            ca_data = kwargs.get('cadata')

            if ca_file or ca_path or ca_data:
                self.ssl_ctx.load_verify_locations(
                    cafile=ca_file, capath=ca_path, cadata=ca_data)
        else:
            self.ssl_ctx = None

    def _setup_ws_url(self, ws_url: str) -> Url:
        url = ws_url.replace("http", "ws", 1)
        return parse_url(f"{url}/deletions")

    def _setup_base_url(self, base_url: Union[Url, str]) -> Url:
        if isinstance(base_url, str):
            base_url = parse_url(base_url)
        if not isinstance(base_url, Url):
            raise ValueError("must be URL or string!")

        return base_url

    async def _websocket_listener(self):
        """
        The WebSocket thread, which waits for messages from Relukko and
        notifies the HTTP thread in case deletions happend, so the HTTP
        can retry to get the lock. Does not verify the wanted lock got
        deleted yet.
        """
        additional_headers = { "X-API-KEY": self.api_key }
        async with ws_connect(
            str(self.ws_url),
            additional_headers=additional_headers,
            ssl=self.ssl_ctx,
            logger=logger,
        ) as websocket:
            while self.ws_running.is_set():
                try:
                    ws_message = await asyncio.wait_for(websocket.recv(), timeout=2)
                    if ws_message:
                        logger.debug("Received message: '%s'", ws_message)
                        msg: Dict = json.loads(ws_message)
                        if msg.get('deletions'):
                            # Signal the HTTP thread to wake up
                            self.message_received.set()
                except TimeoutError:
                    # no messages, try in a moment again...
                    time.sleep(0.5)
                except WsConnectionClosed:
                    logger.error("Lost WS connection!")
                    continue

    def _acquire_relukko(
            self, url: Union[Url, str], max_run_time: int,
            payload: Dict, _thread_store: List):
        """
        The HTTP thread which tries to create the Relukko lock.
        """

        start_time = time.time()

        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > max_run_time:
                self.ws_running.clear()
                _thread_store.insert(0, None)
                return

            res = self._make_request(
                url=url, method="POST", payload=payload)
            if res is None:
                # Conflict 409
                self.message_received.wait(timeout=30)
                self.message_received.clear()
            else:
                _thread_store.insert(0, res)
                self.ws_running.clear()
                return

    def _check_response(self, response: requests.Response):
        match response.status_code:
            case 200 | 201 | 404:
                return response.json()
            case 400 | 403:
                err = response.json()
                logger.warning(err.get('status'), err.get('message'))
                response.raise_for_status()
            case 409:
                err = response.json()
                logger.info(err.get('status'), err.get('message'))
                return None
            case 500 | 502 | 503 | 504:
                logger.warning(response.status_code, response.text)
                raise RelukkoDoRetry()
            case _:
                logger.warning(response.status_code, response.text)
                raise RuntimeError()

    def _make_request(
            self,
            url: str,
            method: str,
            payload: Dict=None) -> requests.Response:

        excpetions = (
            requests.ConnectionError,
            RelukkoDoRetry,
        )

        @retry(logger, exceptions=excpetions, delay=10)
        def _do_request():
            response = self.session.request(
                method=method,
                url=url,
                json=payload,
            )
            return self._check_response(response)

        return _do_request()

    def acquire_relukko(self, lock_name, creator, max_run_time):
        """
        TBD
        """
        payload = {
            "lock_name": lock_name,
            "creator": creator,
        }

        url = f"{self.base_url}/v1/locks/"

        self.ws_running.set()
        self.ws_listener = threading.Thread(
            target=asyncio.run, args=(self._websocket_listener(),))
        self.ws_listener.start()

        thread_store = []
        http_thread = threading.Thread(
            target=self._acquire_relukko, args=(url, max_run_time, payload, thread_store))
        http_thread.start()
        http_thread.join()
        self.ws_listener.join()

        return thread_store[0]

    def get_lock(self, lock_id: str) -> Dict:
        """
        TBD
        """
        url = f"{self.base_url}/v1/locks/{lock_id}"
        return self._make_request(url, "GET")

    def get_locks(self)  -> List:
        """
        TBD
        """
        url = f"{self.base_url}/v1/locks/"
        return self._make_request(url, "GET")

    def update_relukko(self, lock_id: str, creator: str, expires_at: datetime):
        """
        TBD
        """
        if isinstance(expires_at, datetime):
            expires_at = expires_at.isoformat()
        else:
            raise ValueError("has to be datetime!")

        payload = {
            "creator": creator,
            "expires_at": expires_at,
        }
        url = f"{self.base_url}/v1/locks/{lock_id}"
        return self._make_request(url, "POST", payload)

    def delete_relukko(self, lock_id: str):
        """
        TBD
        """
        url = f"{self.base_url}/v1/locks/{lock_id}"
        return self._make_request(url, "DELETE")

    def keep_relukko_alive(self, lock_id: str):
        """
        TBD
        """
        url = f"{self.base_url}/v1/locks/{lock_id}/keep_alive"
        return self._make_request(url, "GET")

    def keep_relukko_alive_put(self, lock_id: str, seconds: int):
        """
        TBD
        """
        url = f"{self.base_url}/v1/locks/{lock_id}/keep_alive"
        payload = {
            "seconds": seconds
        }
        return self._make_request(url, "PUT", payload)

    def add_to_expires_at_time(self, lock_id: str):
        """
        TBD
        """
        url = f"{self.base_url}/v1/locks/{lock_id}/add_to_expire_at"
        return self._make_request(url, "GET")

    def add_to_expires_at_time_put(self, lock_id: str, seconds: int):
        """
        TBD
        """
        url = f"{self.base_url}/v1/locks/{lock_id}/add_to_expire_at"
        payload = {
            "seconds": seconds
        }
        return self._make_request(url, "PUT", payload)
