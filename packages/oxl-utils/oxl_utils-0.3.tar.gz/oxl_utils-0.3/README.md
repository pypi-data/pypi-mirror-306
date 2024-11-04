# Utils Collection

[![Lint](https://github.com/O-X-L/py-utils/actions/workflows/lint.yml/badge.svg)](https://github.com/O-X-L/py-utils/actions/workflows/lint.yml)
[![Test](https://github.com/O-X-L/py-utils/actions/workflows/test.yml/badge.svg)](https://github.com/O-X-L/py-utils/actions/workflows/test.yml)

[pypi.org](https://pypi.org/project/oxl-utils/)

## Install

```bash
pip install oxl-utils
```

----

## Data States

```python3
from oxl_utils.state import is_set
from oxl_utils.state import is_null
```

----

## Network interaction

```python3
# dnspython wrapper
from oxl_utils.net import resolve_dns

# get first IP
from oxl_utils.net import resolve_first_ip

# check if a remote port is reachable
from oxl_utils.net import is_port_open
```

----

## Validators

```python3
# validate email format
from oxl_utils.valid.email import valid_email
from oxl_utils.valid.email import has_mailserver

# ips and networks
from oxl_utils.valid.net import valid_ip
from oxl_utils.valid.net import valid_ip4
from oxl_utils.valid.net import valid_ip6
from oxl_utils.valid.net import valid_net4
from oxl_utils.valid.net import valid_net6
from oxl_utils.valid.net import valid_public_ip
from oxl_utils.valid.net import valid_asn
from oxl_utils.valid.net import valid_port
from oxl_utils.valid.net import get_ipv

# domains
from oxl_utils.valid.dns import valid_domain

# uuid
from oxl_utils.valid.uuid import valid_uuid4
```

----

## Crypto

```python3
# AES CBC
## set secret
from os import environ
environ['CRYPTO_SECRET'] = '<YOUR-SECRET>'

from oxl_utils.crypto.aes_cbc import encrypt
from oxl_utils.crypto.aes_cbc import decrypt
from oxl_utils.crypto.aes_cbc import encrypt_bytes
from oxl_utils.crypto.aes_cbc import decrypt_bytes
```

----

## Processing

```python3
# subprocess wrapper
from oxl_utils.ps import process
## for read-only commands which output should be cached
from oxl_utils.ps import process_cache

# thread handling
from oxl_utils.ps import wait_for_threads
from oxl_utils.ps import process_list_in_threads
```

----

## Django

```python3
# fix datetime timezone
from oxl_utils.dj.dt import datetime_from_db
```
