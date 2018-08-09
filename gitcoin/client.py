"""Define the Gitcoin API client."""

import gitcoin.validation
import requests


class Config:
    """Define Base Class for API Endpoint Config."""

    def __init__(self):
        """Init empty params container."""
        self.params = {}

    def has(self, name):
        """Tell if a setting for 'name' was defined."""
        return name in self.params

    def get(self, name):
        """Get the setting for 'name'."""
        if self.has(name):
            return self.params[name]
        else:
            msg = 'Unknown config "{name}"'
            raise KeyError(msg.format(name=name))


class BountyConfig(Config):
    """Define 'bounties' API Endpoint Config."""

    def __init__(self):
        """Init params container for 'bounties' filters etc."""
        super().__init__()
        self.params = {
            'experience_level': (True, gitcoin.validation.experience_level),
            'project_length': (True, gitcoin.validation.project_length),
            'bounty_type': (True, gitcoin.validation.bounty_type),
            'bounty_owner_address': (True, str),
            'bounty_owner_github_username': (True, str),
            'idx_status': (True, gitcoin.validation.idx_status),
            'network': (True, str),
            'standard_bounties_id': (True, int),
            'pk__gt': (False, int),
            'started': (False, str),
            'is_open': (False, bool),
            'github_url': (True, str),
            'fulfiller_github_username': (False, str),
            'interested_github_username': (False, str),
            'raw_data': (True, str),
            'order_by': (False, gitcoin.validation.order_by),
            'limit': (False, int),
            'offset': (False, int)
        }


class Endpoint:
    """Wrap one Gitcoin API end point."""

    def __init__(self, url, config):
        """Inject URL and Config, default to no query parameters."""
        self.url = url
        self.config = config
        self.params = {}

    def _add_param(self, name, value):
        """Add query parameter with safeguards."""
        if self.config.has(name):
            is_multiple, normalize = self.config.get(name)
            if not is_multiple:
                self._del_param(name)  # Throw away all previous values, if any.
            if callable(normalize):
                value = normalize(value)
            self._add_param_unchecked(name, value)
            return self
        else:
            msg = 'Tried to filter by unknown param "{name}".'
            raise KeyError(msg.format(name=name))

    def _del_param(self, name):
        """Delete query parameter."""
        if name in self.params:
            del self.params[name]
        return self

    def _reset_all_params(self):
        """Delete all query parameters."""
        self.params = {}

    def _add_param_unchecked(self, name, value):
        """Add query parameter without safeguards.

        This is available in case this API client is out-of-sync with the API.
        """
        if name not in self.params:
            self.params[name] = []
        self.params[name].append(str(value))
        return self

    def filter(self, **kwargs):
        """Filter the result set."""
        for name, value in kwargs.items():
            self._add_param(name, value)
        return self

    def order_by(self, sort):
        """Sort the result set."""
        self._add_param('order_by', sort)
        return self

    def get_page(self, number=1, per_page=25):
        """Get one page of the resources list."""
        self._add_param('limit', per_page)
        self._add_param('offset', (number - 1) * per_page)
        return self._request_get()

    def all(self):
        """List all resources."""
        self._del_param('limit')
        self._del_param('offset')
        return self._request_get()

    def get(self, primary_key):
        """Retrieve one resource by primary key."""
        return self._request_get(''.join((self.url, str(primary_key))))

    def _request_get(self, url=None):
        """Fire the actual HTTP GET request as configured."""
        url = url if url else self.url
        params = self._prep_get_params()
        response = requests.get(url, params=params)
        response.raise_for_status()  # Let API consumer know about HTTP errors.
        return response.json()

    def _prep_get_params(self):
        """Send multi-value fields separated by comma."""
        return {name: ','.join(value) for name, value in self.params.items()}


class Gitcoin:
    """Provide main API entry point."""

    def __init__(self):
        """Set defaults."""
        self.classes = {}
        self.set_class('endpoint', Endpoint)
        self.set_class('bounties_list_config', BountyConfig)
        self.urls = {}
        self.set_url('bounties', 'https://gitcoin.co/api/v0.1/bounties/')

    def set_class(self, cls_id, cls):
        """Inject class dependency, overriding the default class."""
        self.classes[cls_id] = cls

    def set_url(self, cls_id, url):
        """Configure API URL, overriding the default URL."""
        self.urls[cls_id] = url

    @property
    def bounties(self):
        """Wrap the 'bounties' API endpoint."""
        url = self.urls['bounties']
        endpoint_class = self.classes['endpoint']
        config_class = self.classes['bounties_list_config']
        return endpoint_class(url, config_class())
