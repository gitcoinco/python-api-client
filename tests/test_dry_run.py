import urllib.parse

import pytest
import requests
import requests.exceptions
import responses
from gitcoin import BountyConfig, Gitcoin

pymark = pytest.mark.pytestconfig


def are_url_queries_equal(url1, url2, *more_urls):
    queries = []
    urls = [url1, url2]
    urls.extend(more_urls)
    for url in urls:
        query_string = urllib.parse.urlparse(url).query
        query = urllib.parse.parse_qs(query_string)
        queries.append(query)
    for i in range(1, len(queries)):
        if not (queries[i - 1] == queries[i]):
            return False
    return True


class TestGitcoinDryRun():

    def test_are_url_queries_equal(self):
        assert are_url_queries_equal('https://google.com', 'https://google.com')
        assert not are_url_queries_equal('https://google.com?q=1', 'https://google.com?q=2')
        assert not are_url_queries_equal('https://google.com?q=1', 'https://google.com?q=2', 'https://google.com?q=3')
        assert not are_url_queries_equal(
            'https://google.com?q=1', 'https://google.com?q=2', 'https://google.com?q=3', 'https://google.com?q=4'
        )
        assert are_url_queries_equal('https://google.com?q=1', 'https://google.com?q=1', 'https://google.com?q=1')
        assert are_url_queries_equal(
            'https://google.com?q=1', 'https://google.com?q=1', 'https://google.com?q=1', 'https://google.com?q=1'
        )
        assert are_url_queries_equal('https://google.com?q=1&r=2', 'https://google.com?r=2&q=1')
        with pytest.raises(TypeError):
            are_url_queries_equal('https://google.com?q=1')

    def test_cfg_raises_on_unknown_param(self):
        cfg = BountyConfig()
        with pytest.raises(KeyError):
            cfg.get('does_not_exist')

    def test_api_raises_on_unknown_param(self):
        api = Gitcoin()
        with pytest.raises(KeyError):
            api.bounties.filter(does_not_exist=True)

    @classmethod
    def test_all(cls, responses):
        responses.add(responses.GET, 'https://gitcoin.co/api/v0.1/bounties/', json={'mock': 'mock'}, status=200)
        api = Gitcoin()
        result = api.bounties.all()
        assert result == {'mock': 'mock'}
        assert len(responses.calls) == 1
        assert are_url_queries_equal(responses.calls[0].request.url, 'https://gitcoin.co/api/v0.1/bounties/')

    @classmethod
    def test_filter_pk__gt(cls, responses):
        responses.add(responses.GET, 'https://gitcoin.co/api/v0.1/bounties/', json={'mock': 'mock'}, status=200)
        api = Gitcoin()
        result = api.bounties.filter(pk__gt=100).all()
        assert result == {'mock': 'mock'}
        assert len(responses.calls) == 1
        assert are_url_queries_equal(responses.calls[0].request.url, 'https://gitcoin.co/api/v0.1/bounties/?pk__gt=100')

    @classmethod
    def test_filter_experience_level(cls, responses):
        responses.add(responses.GET, 'https://gitcoin.co/api/v0.1/bounties/', json={'mock': 'mock'}, status=200)
        api = Gitcoin()
        result = api.bounties.filter(experience_level='Beginner').all()
        assert result == {'mock': 'mock'}
        assert len(responses.calls) == 1
        assert are_url_queries_equal(
            responses.calls[0].request.url, 'https://gitcoin.co/api/v0.1/bounties/?experience_level=Beginner'
        )
        with pytest.raises(ValueError):
            api.bounties.filter(experience_level='Rockstar')

    @classmethod
    def test_filter_project_length(cls, responses):
        responses.add(responses.GET, 'https://gitcoin.co/api/v0.1/bounties/', json={'mock': 'mock'}, status=200)
        api = Gitcoin()
        result = api.bounties.filter(project_length='Hours').all()
        assert result == {'mock': 'mock'}
        assert len(responses.calls) == 1
        assert are_url_queries_equal(
            responses.calls[0].request.url, 'https://gitcoin.co/api/v0.1/bounties/?project_length=Hours'
        )
        with pytest.raises(ValueError):
            api.bounties.filter(project_length='Minutes')

    @classmethod
    def test_filter_bounty_type(cls, responses):
        responses.add(responses.GET, 'https://gitcoin.co/api/v0.1/bounties/', json={'mock': 'mock'}, status=200)
        api = Gitcoin()
        result = api.bounties.filter(bounty_type='Bug').all()
        assert result == {'mock': 'mock'}
        assert len(responses.calls) == 1
        assert are_url_queries_equal(
            responses.calls[0].request.url, 'https://gitcoin.co/api/v0.1/bounties/?bounty_type=Bug'
        )
        with pytest.raises(ValueError):
            api.bounties.filter(bounty_type='Fancy')

    @classmethod
    def test_filter_idx_status(cls, responses):
        responses.add(responses.GET, 'https://gitcoin.co/api/v0.1/bounties/', json={'mock': 'mock'}, status=200)
        api = Gitcoin()
        result = api.bounties.filter(idx_status='started').all()
        assert result == {'mock': 'mock'}
        assert len(responses.calls) == 1
        assert are_url_queries_equal(
            responses.calls[0].request.url, 'https://gitcoin.co/api/v0.1/bounties/?idx_status=started'
        )
        with pytest.raises(ValueError):
            api.bounties.filter(idx_status='undone')

    @classmethod
    def test_filter_2x_bounty_type_paged(cls, responses):
        responses.add(responses.GET, 'https://gitcoin.co/api/v0.1/bounties/', json={'mock': 'mock'}, status=200)
        api = Gitcoin()
        result = api.bounties.filter(bounty_type='Feature').filter(bounty_type='Bug').get_page()
        assert result == {'mock': 'mock'}
        assert len(responses.calls) == 1
        assert are_url_queries_equal(
            responses.calls[0].request.url,
            'https://gitcoin.co/api/v0.1/bounties/?bounty_type=Feature%2CBug&offset=0&limit=25'
        )

    @classmethod
    def test_del_param(cls, responses):
        responses.add(responses.GET, 'https://gitcoin.co/api/v0.1/bounties/', json={'mock': 'mock'}, status=200)
        res = Gitcoin().bounties.filter(bounty_type='Feature')
        res._del_param('bounty_type').filter(bounty_type='Bug').get_page()
        assert res == {'mock': 'mock'}
        assert len(responses.calls) == 1
        assert are_url_queries_equal(
            responses.calls[0].request.url,
            'https://gitcoin.co/api/v0.1/bounties/?bounty_type=Bug&offset=0&limit=25'
        )

    @classmethod
    def test_reset_all_params(cls, responses):
        responses.add(responses.GET, 'https://gitcoin.co/api/v0.1/bounties/', json={'mock': 'mock'}, status=200)
        api = Gitcoin()
        bounties_api = api.bounties

        result = bounties_api.filter(bounty_type='Feature').get_page()
        assert result == {'mock': 'mock'}
        assert len(responses.calls) == 1
        assert are_url_queries_equal(
            responses.calls[0].request.url,
            'https://gitcoin.co/api/v0.1/bounties/?bounty_type=Feature&offset=0&limit=25'
        )

        bounties_api._reset_all_params()

        result = bounties_api.filter(bounty_type='Bug').get_page()
        assert result == {'mock': 'mock'}
        assert len(responses.calls) == 2
        assert are_url_queries_equal(
            responses.calls[1].request.url, 'https://gitcoin.co/api/v0.1/bounties/?bounty_type=Bug&offset=0&limit=25'
        )

    @classmethod
    def test_order_by(cls, responses):
        responses.add(responses.GET, 'https://gitcoin.co/api/v0.1/bounties/', json={'mock': 'mock'}, status=200)
        api = Gitcoin()

        result = api.bounties.order_by('-project_length').get_page()
        assert result == {'mock': 'mock'}
        assert len(responses.calls) == 1
        assert are_url_queries_equal(
            responses.calls[0].request.url,
            'https://gitcoin.co/api/v0.1/bounties/?order_by=-project_length&offset=0&limit=25'
        )

        result = api.bounties.order_by('is_open').get_page()
        assert result == {'mock': 'mock'}
        assert len(responses.calls) == 2
        assert are_url_queries_equal(
            responses.calls[1].request.url,
            'https://gitcoin.co/api/v0.1/bounties/?order_by=is_open&offset=0&limit=25'
        )

        with pytest.raises(ValueError):
            api.bounties.order_by('random')

    @classmethod
    def test_get(cls, responses):
        responses.add(responses.GET, 'https://gitcoin.co/api/v0.1/bounties/123', json={'mock': 'mock'}, status=200)
        api = Gitcoin()
        result = api.bounties.get(123)
        assert result == {'mock': 'mock'}
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == 'https://gitcoin.co/api/v0.1/bounties/123'

    @classmethod
    def test_no_normalize(cls, responses):

        class ExtendedBountyConfig(BountyConfig):

            def __init__(self):
                super().__init__()
                self.params['no_normalize'] = (True, None)

        api = Gitcoin()
        api.set_class('bounties_list_config', ExtendedBountyConfig)

        responses.add(responses.GET, 'https://gitcoin.co/api/v0.1/bounties/', json={'mock': 'mock'}, status=200)

        result = api.bounties.filter(no_normalize='not_normal').get_page()
        assert result == {'mock': 'mock'}
        assert len(responses.calls) == 1
        assert are_url_queries_equal(
            responses.calls[0].request.url,
            'https://gitcoin.co/api/v0.1/bounties/?no_normalize=not_normal&offset=0&limit=25'
        )

    @classmethod
    def test_raise_for_status(cls, responses):
        responses.add(responses.GET, 'https://gitcoin.co/api/v0.1/bounties/', json={'mock': 'mock'}, status=401)
        api = Gitcoin()
        with pytest.raises(requests.exceptions.HTTPError):
            result = api.bounties.all()

    def test_extending_config_does_not_leak(self):

        class ExtendedBountyConfig(BountyConfig):

            def __init__(self):
                super().__init__()
                self.params['extra_config'] = (True, None)

        extended_bounty_config = ExtendedBountyConfig()
        normal_bounty_config = BountyConfig()
        with pytest.raises(KeyError):
            normal_bounty_config.get('extra_config')
