from unittest.mock import MagicMock

import pytest

from utils.db_adapter import DbAdapter


class _MockAdapter(DbAdapter):
    def connect(self):
        self.connection = MagicMock()


@pytest.fixture(scope='function')
def adapter():
    return _MockAdapter('localhost', 'fake', 'fake')


@pytest.fixture(scope='function')
def connected_adapter(adapter: DbAdapter):
    adapter.connect()
    return adapter


class TestConnectDisconnect:
    def test_initial_state(self, adapter: DbAdapter):
        assert not adapter.is_connected

    def test_connect(self, connected_adapter: DbAdapter):
        assert connected_adapter.is_connected

    def test_disconnect(self, connected_adapter: DbAdapter):
        connected_adapter.disconnect()
        assert not connected_adapter.is_connected
