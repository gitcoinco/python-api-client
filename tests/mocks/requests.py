

class MockResponse:
    def __init__(self, url, params, kwargs):
        self.url = url
        self.params = params
        self.kwargs = kwargs

    def json(self):
        return {
            'url': self.url,
            'params': self.params,
            'kwargs': self.kwargs,
        }

    def raise_for_status(self):
        if 'raise_for_status' in self.params:
            if self.params['raise_for_status']:
                raise ValueError('Mock HTTP Error')
