import pytest
import requests
from gitcoin import BountyConfig, Gitcoin
from tests.mocks.requests import MockResponse


def mock_requests_get(url, params=None, **kwargs):
    return MockResponse(url, params, kwargs)


class TestGitcoinDryRun():

    @pytest.fixture(autouse=True)
    def no_requests(self, monkeypatch):
        monkeypatch.setattr(requests, 'get', mock_requests_get)

    def test_cfg_raises_on_unknown_param(self):
        cfg = BountyConfig()
        with pytest.raises(KeyError):
            cfg.get('does_not_exist')

    def test_api_raises_on_unknown_param(self):
        api = Gitcoin()
        with pytest.raises(KeyError):
            api.bounties.filter(does_not_exist=True)

    def test_all(self):
        api = Gitcoin()
        expected = {
            'url': 'https://gitcoin.co/api/v0.1/bounties',
            'params': {},
            'kwargs': {},
        }
        result = api.bounties.all()
        assert expected == result

    def test_filter_pk__gt(self):
        api = Gitcoin()
        expected = {
            'url': 'https://gitcoin.co/api/v0.1/bounties',
            'params': {
                'pk__gt': '100'
            },
            'kwargs': {},
        }
        result = api.bounties.filter(pk__gt=100).all()
        assert expected == result

    def test_filter_2x_bounty_type_paged(self):
        api = Gitcoin()
        expected = {
            'url': 'https://gitcoin.co/api/v0.1/bounties',
            'params': {
                'bounty_type': 'Feature,Bug',
                'offset': '0',
                'limit': '25',
            },
            'kwargs': {},
        }
        result = api.bounties.filter(bounty_type='Feature').filter(bounty_type='Bug').get_page()
        assert expected == result

    def test_del_param(self):
        api = Gitcoin()
        expected = {
            'url': 'https://gitcoin.co/api/v0.1/bounties',
            'params': {
                'bounty_type': 'Bug',
                'offset': '0',
                'limit': '25',
            },
            'kwargs': {},
        }
        result = api.bounties.filter(bounty_type='Feature').del_param('bounty_type').filter(bounty_type='Bug').get_page()
        assert expected == result

    def test_order_by(self):
        api = Gitcoin()
        expected = {
            'url': 'https://gitcoin.co/api/v0.1/bounties',
            'params': {
                'order_by': '-project_length',
                'offset': '0',
                'limit': '25',
            },
            'kwargs': {},
        }
        result = api.bounties.order_by('-project_length').get_page()
        assert expected == result

    def test_get(self):
        api = Gitcoin()
        expected = {
            'url': 'https://gitcoin.co/api/v0.1/bounties/123',
            'params': {},
            'kwargs': {},
        }
        result = api.bounties.get(123)
        assert expected == result

    def test_no_normalize(self):
        class ExtendedBountyConfig(BountyConfig):
            def __init__(self):
                self.params['no_normalize'] = (True, None)

        api = Gitcoin()
        api.set_class('bounties_list_config', ExtendedBountyConfig)
        expected = {
            'url': 'https://gitcoin.co/api/v0.1/bounties',
            'params': {
                'no_normalize': 'not_normal',
                'offset': '0',
                'limit': '25',
            },
            'kwargs': {},
        }
        result = api.bounties.filter(no_normalize='not_normal').get_page()
        assert expected == result

    def test_raise_for_status(self):
        api = Gitcoin()
        with pytest.raises(ValueError):  # ValueError only in mock setup
            result = api.bounties.add_param_unchecked('raise_for_status', True).all()
