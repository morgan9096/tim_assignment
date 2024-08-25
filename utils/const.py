from pathlib import Path


class TestOptions:
    URL = '--url'


class Paths:
    _ROOT = Path(__file__).parent.parent
    TEST_LOG = _ROOT / 'test.log'


API_URL = 'https://jsonplaceholder.typicode.com'
