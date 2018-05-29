import gitcoin.validation
import pytest
import requests
from gitcoin import BountyConfig, Gitcoin


def assert_is_list_of_bounties(result):
    assert list == type(result)
    for bounty in result:
        assert_is_bounty(bounty)

def assert_is_bounty(bounty):
    assert int == type(bounty['pk'])
    assert 0 < bounty['pk']


@pytest.mark.skipif(not pytest.config.getoption('--liveapi'), reason='Please only test against the live API manually by specifying --live-api.')
class TestGitcoinLiveBounties():

    filter_examples = {
        # 'raw_data': ['"'],  ## It's unclear what good examples would be.
        'experience_level': ['Beginner', 'Advanced', 'Intermediate', 'Unknown'],
        'project_length': ['Hours', 'Days', 'Weeks', 'Months', 'Unknown'],
        'bounty_type': ['Bug', 'Security', 'Feature', 'Unknown'],
        'bounty_owner_address': ['0x4331b095bc38dc3bce0a269682b5ebaefa252929'],
        'bounty_owner_github_username': ['owocki'],
        'idx_status': ['cancelled', 'done', 'expired', 'open', 'started', 'submitted', 'unknown'],
        'network': ['mainnet', 'rinkeby'],
        'standard_bounties_id': [45, 215],
        'pk__gt': [3270],
        'started': ['owocki'],
        'is_open': [True, False],
        'github_url': ['https://github.com/gitcoinco/web/issues/805'],
        'fulfiller_github_username': ['owocki'],
        'interested_github_username': ['owocki'],
    }

    def test_filter_examples(self):
        api = Gitcoin()
        for filter_name, examples in self.filter_examples.items():
            for example in examples:
                filter = {filter_name:example}
                # try:
                result = api.bounties.filter(**filter).get_page(per_page=1)
                # except
                assert_is_list_of_bounties(result)

    def test_multiple_value_filters(self):
        api = Gitcoin()
        cfg = BountyConfig()
        for filter_name, examples in self.filter_examples.items():
            is_multiple, normalize = cfg.get(filter_name)
            if is_multiple:
                bounties = api.bounties
                for example in examples:
                    filter = {filter_name:example}
                    bounties.filter(**filter)
                result = bounties.get_page(per_page=1)
                assert_is_list_of_bounties(result)

    def test_order_by(self):
        sort_field_names = gitcoin.validation.options['order_by']
        api = Gitcoin()
        for field_name in sort_field_names:
            for direction in [field_name, ''.join(('-', field_name))]:
                result = api.bounties.order_by(direction).get_page(per_page=1)
                assert_is_list_of_bounties(result)
