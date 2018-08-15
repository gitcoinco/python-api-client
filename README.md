# Gitcoin Python API Client

[![Build Status](https://travis-ci.com/gitcoinco/python-api-client.svg?branch=master)](https://travis-ci.com/gitcoinco/python-api-client)

This Python package provides the `bounties` endpoint of the Gitcoin API, which allows you to:

- list all bounties
- list all bounties which meet certain conditions (i.e. filter them)
- retrieve a single bounty by it's primary key

## Install via pypi

```bash
pip install gitcoin
```

## Usage Examples

### List all bounties

```python
from gitcoin import Gitcoin
api = Gitcoin()
all_bounties = api.bounties.all()
```

### List all open bounties

```python
from gitcoin import Gitcoin
api = Gitcoin()
open_bounties = api.bounties.filter(is_open=True).all()
```

### List all open "Beginner" bounties

```python
from gitcoin import Gitcoin
api = Gitcoin()
bounties_api = api.bounties
bounties_api.filter(is_open=True)
bounties_api.filter(experience_level='Beginner')
open_beginner_bounties = bounties_api.all()
```

The example above has been reformatted for easier reading. A [fluent interface](https://en.wikipedia.org/wiki/Fluent_interface#Python) is also available. Please scroll the following code block all the way to the end to see the whole line:

```python
from gitcoin import Gitcoin
api = Gitcoin()
open_beginner_bounties = api.bounties.filter(is_open=True, experience_level='Beginner').all()
```

### List all open bounties marked for either "Beginner" OR "Intermediate" experience level

For some filter conditions, multiple different values can be given, which results in a logical `OR` for that condition:

```python
from gitcoin import Gitcoin
api = Gitcoin()
bounties_api = api.bounties
bounties_api.filter(is_open=True)
bounties_api.filter(experience_level='Beginner')
bounties_api.filter(experience_level='Intermediate')
open_beginner_and_intermediate_bounties = bounties_api.all()
```

The example above has been reformatted for easier reading. A [fluent interface](https://en.wikipedia.org/wiki/Fluent_interface#Python) is also available. Please scroll the following code block all the way to the end to see the whole line:

```python
from gitcoin import Gitcoin
api = Gitcoin()
open_beginner_and_intermediate_bounties = api.bounties.filter(is_open=True).filter(experience_level='Beginner').filter(experience_level='Intermediate').all()
```

## API

### Instantiation

1. Create a `Gitcoin()` API root object:
```python
from gitcoin import Gitcoin
api = Gitcoin()
```
2. The `bounties` API endpoint is accessible as a property of the API root object:
```python
bounties_endpoint = api.bounties
```
Each access to the `bounties` property results in a new `Endpoint` object with no filter conditions or any other parameters (like sorting) set. If you want to keep a specific set of filter conditions, simply store the `Endpoint` object in a variable instead of referring to the `bounties` property of the root object.

### `bounties.filter(**kwargs)`

Limit the list of bounties returned by either `get_page()` or `all()` to those bounties meeting the filter condition(s). For some filter conditions, multiple different values can be given, which results in a logical `OR` for that condition.

The condition name is the name of the keyword argument, and the condition value is the value of the keyword argument:

```python
open_bounties = api.bounties.filter(is_open=True).all()
```

Conditions with different names can be given in one `filter()` call:

```python
open_beginner bounties = api.bounties.filter(is_open=True, experience_level='Beginner').all()
```

Or if preferred, they can also be given in separate `filter()` calls:

```python
open_beginner bounties = api.bounties.filter(is_open=True).filter(experience_level='Beginner').all()
```

Giving multiple values for the same filter condition has to be done in separate calls to `filter()`:

```python
beginner_and_intermediate_bounties = api.bounties.filter(experience_level='Beginner').filter(experience_level='Intermediate').all()
```

For the following filter conditions, multiple values can be given to achieve a logical `OR`:

- `experience_level (str)`
- `project_length (str)`
- `bounty_type (str)`
- `bounty_owner_address (str)`
- `bounty_owner_github_username (str)`
- `idx_status (str)`
- `network (str)`
- `standard_bounties_id (int)`
- `github_url (str)`
- `raw_data (str)`

The following filter conditions are **single value**, in other words, multiple values result in the last value overwriting all earlier values:

- `pk__gt (int)`
- `started (str)`
- `is_open (bool)`
- `fulfiller_github_username (str)`
- `interested_github_username (str)`

`filter()` returns the `Endpoint` object itself to enable a [fluent interface](https://en.wikipedia.org/wiki/Fluent_interface#Python).

### `bounties.order_by(sort)`

Determine the order of the bounties returned by either `get_page()` or `all()`. The `sort` argument is a `string` containing a DB field name to sort by. It can also have an optional "-" prefix for reversing the direction. Choose from these field names:

- `accepted`
- `balance`
- `bounty_owner_address`
- `bounty_owner_email`
- `bounty_owner_github_username`
- `bounty_owner_name`
- `bounty_type`
- `canceled_on`
- `contract_address`
- `current_bounty`
- `experience_level`
- `expires_date`
- `fulfillment_accepted_on`
- `fulfillment_started_on`
- `fulfillment_submitted_on`
- `github_comments`
- `github_url`
- `idx_experience_level`
- `idx_project_length`
- `idx_status`
- `interested`
- `interested_comment`
- `is_open`
- `issue_description`
- `last_comment_date`
- `metadata`
- `network`
- `num_fulfillments`
- `override_status`
- `privacy_preferences`
- `project_length`
- `raw_data`
- `snooze_warnings_for_days`
- `standard_bounties_id`
- `submissions_comment`
- `title`
- `token_address`
- `token_name`
- `token_value_in_usdt`
- `token_value_time_peg`
- `_val_usd_db`
- `value_in_eth`
- `value_in_token`
- `value_in_usdt`
- `value_in_usdt_now`
- `value_true`
- `web3_created`
- `web3_type`

`order_by()` returns the `Endpoint` object itself to enable a [fluent interface](https://en.wikipedia.org/wiki/Fluent_interface#Python).

### `bounties.get_page(number=1, per_page=25)`

Returns one page of the (potentially `filter()`ed) `list` of bounties with the given 1-based index `number (int)`. The page size can be set with `per_page (int)`. Each bounty is a `dict`, basically the direct output of [`requests`' `.json()`](http://docs.python-requests.org/en/master/user/quickstart/#json-response-content) call.

### `bounties.all()`

Returns the complete (potentially `filter()`ed) `list` of bounties. Each bounty is a `dict`, basically the direct output of [`requests`' `.json()`](http://docs.python-requests.org/en/master/user/quickstart/#json-response-content) call.

### `bounties.get(primary_key)`

Returns one (1) bounty as specified by `primary_key (int)`. It is returned as a `dict`, basically the direct output of [`requests`' `.json()`](http://docs.python-requests.org/en/master/user/quickstart/#json-response-content) call.

-------------------------

## Todo

- [x] Add base gitcoin.Gitcoin client
- [x] Add `bounties` api filter
  - [x] Implement all filter fields present in `gitcoinco/web/app/dashboard/router.py`
- [ ] Add `universe` api filter
  - [ ] Implement all filter fields present in `gitcoinco/web/app/external_bounties/router.py`
- [x] Add sorting/order_by
- [x] Add pagination (page/limit)
- [ ] Add travis-ci.com project and twine/pypi credentials.
- [ ] Add codecov.io project.
- [ ] Cut first release (Tag github release, push changes, and let CI deploy to pypi)
- [ ] Maintain +90% coverage
