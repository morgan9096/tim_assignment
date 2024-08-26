from unittest.mock import MagicMock

import pytest

from utils.db_adapter import DbAdapter


_DB_NAME = 'test_db'
_TABLE_NAME = 'test_table'
_TABLE_DATA = (
    "CREATE TABLE `employees` ("
    "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ENGINE=InnoDB"
)


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


def test_create_and_drop_table(connected_adapter: DbAdapter):
    connected_adapter.create_db(_DB_NAME)
    connected_adapter.create_table(_DB_NAME, _TABLE_NAME, _TABLE_DATA)
    assert _TABLE_NAME in connected_adapter.get_tables(_DB_NAME)
    connected_adapter.drop_table(_DB_NAME, _TABLE_NAME)
    assert _TABLE_NAME not in connected_adapter.get_tables(_DB_NAME)
