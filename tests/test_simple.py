# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import pathlib
import unittest
from http_request import http_request
from utils import path_util


class TestSimple(unittest.TestCase):
    def test_http_request(self):
        http_request.start()

    def test_path_util(self):
        here = pathlib.Path(__file__).parent.resolve()
        print(here)


if __name__ == '__main__':
    unittest.main()
