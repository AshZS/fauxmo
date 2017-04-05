"""conftest.py :: Setup fixtures for pytest."""

from multiprocessing import Process
from time import sleep
from typing import Generator

from fauxmo import fauxmo

import httpbin
import pytest


@pytest.fixture(scope="session")
def fauxmo_server() -> Generator:
    config_path_str = "tests/test_config.json"
    server = Process(target=fauxmo.main,
                     kwargs={'config_path_str': config_path_str},
                     daemon=True)

    server.start()
    sleep(1)

    yield

    server.terminate()
    server.join()


@pytest.fixture(scope="function")
def simplehttpplugin_server() -> Generator:
    fauxmo_device = Process(target=httpbin.core.app.run,
                            kwargs={"host": "127.0.0.1", "port": 8000},
                            daemon=True)

    fauxmo_device.start()
    sleep(1)

    yield

    fauxmo_device.terminate()
    fauxmo_device.join()
