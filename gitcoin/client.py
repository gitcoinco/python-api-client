import requests


class Config:
    """Define Base Class for API Endpoint Config."""
    params = {}

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
    params = {
        'raw_data': (True, str),
        'experience_level': (True, str),
        'project_length': (True, str),
        'bounty_type': (True, str),
        'bounty_owner_address': (True, str),
        'idx_status': (True, str),
        'network': (True, str),
        'bounty_owner_github_username': (True, str),
        'standard_bounties_id': (True, str),
        'pk__gt': (False, int),
        'started': (False, str),
        'is_open': (False, bool),
        'github_url': (True, str),
        'fulfiller_github_username': (False, str),
        'interested_github_username': (False, str),
        'order_by': (False, str),
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

    def add_param(self, name, value):
        """Add query parameter with safeguards."""
        if self.config.has(name):
            is_multiple, normalize = self.config.get(name)
            if not is_multiple:
                self.del_param(name)  # Throw away all previous values, if any.
            if callable(normalize):
                value = normalize(value)
            self.add_param_unchecked(name, value)
            return self
        else:
            msg = 'Tried to filter by unknown param "{name}".'
            raise KeyError(msg.format(name=name))

    def del_param(self, name):
        """Delete query parameter."""
        if name in self.params:
            del self.params[name]
        return self

    def add_param_unchecked(self, name, value):
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
            self.add_param(name, value)
        return self

    def order_by(self, sort):
        """Sort the result set."""
        self.add_param('order_by', sort)
        return self

    def get_page(self, number=1, per_page=25):
        """Get a page of the result set."""
        self.add_param('limit', per_page)
        self.add_param('offset', (number - 1) * per_page)
        return self._request_get()

    def all(self):
        """Get the complete result set."""
        self.del_param('limit')
        self.del_param('offset')
        return self._request_get()

    def get(self, pk):
        """Get 1 object by primary key."""
        return self._request_get('/'.join((self.url, str(pk))))

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
        self.set_url('bounties', 'https://gitcoin.co/api/v0.1/bounties')

    def set_class(self, id, cls):
        """Inject class dependency, overriding the default class."""
        self.classes[id] = cls

    def set_url(self, id, url):
        """Configure API URL, overriding the default URL."""
        self.urls[id] = url

    @property
    def bounties(self):
        """Wrap the 'bounties' API endpoint."""
        url = self.urls['bounties']
        endpointClass = self.classes['endpoint']
        configClass = self.classes['bounties_list_config']
        return endpointClass(url, configClass())
