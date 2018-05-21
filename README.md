# python-api-client
Python API Client

## Install via pypi

```bash
pip install gitcoin
```

## Usage

```python
from gitcoin import Gitcoin
api = Gitcoin()
api.bounties.all()
api.bounties.filter(pk__gt=100).all()
```

## API

### public (unrestricted)

`GET /api/v2/bounties`

### private (restricted)


## Todo

- [ ] Add base gitcoin.Gitcoin client
- [ ] Add `bounties` api filter
  - [ ] Implement all filter fields present in `gitcoinco/web/app/dashboard/router.py`
- [ ] Add `universe` api filter
  - [ ] Implement all filter fields present in `gitcoinco/web/app/external_bounties/router.py`
- [ ] Add sorting/order_by
- [ ] Add pagination (page/limit)
- [ ] Add travis-ci.com project and twine/pypi credentials.
- [ ] Add codecov.io project.
- [ ] Cut first release (Tag github release, push changes, and let CI deploy to pypi)
- [ ] Maintain +90% coverage
