import pytest


# see https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
def pytest_addoption(parser):
    parser.addoption('--liveapi', action='store_true', default=False, help='run some tests againts live API')
