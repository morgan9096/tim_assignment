import random

import allure
import pytest

from utils.const import API_URL, TestOptions
from utils.logger import log
from utils.request import collect_get_response


def pytest_addoption(parser):
    parser.addoption(TestOptions.URL, action='store', default=API_URL)


@pytest.fixture(scope='session')
def url_for_test(pytestconfig: pytest.Config) -> str:
    return pytestconfig.getoption(TestOptions.URL)


@pytest.fixture(scope='session')
def user_id(url_for_test: str) -> int:
    """
    Retrieve a random user (userID), 
    print out its email address to the console in the Allure Report.
    """
    allure.dynamic.epic(f'Testing api for {url_for_test}')
    url = f'{url_for_test}/users'
    with allure.step(f'Get users data from url: {url}'):
        response = collect_get_response(url)
        assert response.ok, f'Failed to get data from {url}'
    users_list = response.json()
    user_id = random.randint(0, len(users_list) - 1)
    user_data = users_list[user_id]
    assert user_data
    log.debug(f'Collected user data: {user_data}')
    allure.dynamic.title(f'Use user {user_data["email"]}')
    return user_id
