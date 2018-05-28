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


class TestGitcoinLiveBountiesAllFilters():

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
                result = api.bounties.filter(**filter).get_page(per_page=1)
                assert_is_list_of_bounties(result)
                # assert list == type(result)
                # if len(result):
                #     assert int == type(result[0]['pk'])
                #     assert 0 < result[0]['pk']

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
                # assert list == type(result)
                # if len(result):
                #     assert int == type(result[0]['pk'])
                #     assert 0 < result[0]['pk']

    def test_order_by(self):
        sort_field_names = [
            'web3_type', 'title', 'web3_created', 'value_in_token',
            'token_name', 'token_address', 'bounty_type', 'project_length',
            'experience_level', 'github_url', 'github_comments',
            'bounty_owner_address', 'bounty_owner_email',
            'bounty_owner_github_username', 'bounty_owner_name', 'is_open',
            'expires_date', 'raw_data', 'metadata', 'current_bounty',
            '_val_usd_db', 'contract_address', 'network',
            'idx_experience_level', 'idx_project_length', 'idx_status',
            'issue_description', 'standard_bounties_id', 'num_fulfillments',
            'balance', 'accepted', 'interested', 'interested_comment',
            'submissions_comment', 'override_status', 'last_comment_date',
            'fulfillment_accepted_on', 'fulfillment_submitted_on',
            'fulfillment_started_on', 'canceled_on',
            'snooze_warnings_for_days', 'token_value_time_peg',
            'token_value_in_usdt', 'value_in_usdt_now', 'value_in_usdt',
            'value_in_eth', 'value_true', 'privacy_preferences'
        ]
        api = Gitcoin()
        for field_name in sort_field_names:
            for direction in [field_name, ''.join(('-', field_name))]:
                result = api.bounties.order_by(direction).get_page(per_page=1)
                assert_is_list_of_bounties(result)
