# Firezone Client

Manage your Firezone with its api.

## Installation

```bash
pip install firezone-client
```

## Init client & List users

```python
from firezone_client import FZclient, User

endpoint = "http://localhost:13000/v0"
token = "0123456789abcdef"
client = FZClient(endpoint, token)

users = client.list(User)

for user in users:
    print(user.email)
```

Read more for how to use the client in the [docs](https://msterhuj.github.io/firezone-client/)
