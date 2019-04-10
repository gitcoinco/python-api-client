import pytest


# see https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
def pytest_addoption(parser):
    parser.addoption('--live-api', action='store_true', default=False, help='run some tests against live API')
