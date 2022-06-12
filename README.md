# IPRoyal Pawns API

UNOFFICIAL Python bindings for IPRoyal Pawns Dashboard API

## Installation

```BASH
pip install pyIPRoyalPawns
```

## Usage

---

### Login with username and password:

```PYTHON
from pyIPRoyalPawns import IPRoyalPawns

# Your IPRoyalPawns (IPR) login username/email and password
USERNAME = ""
PASSWORD = ""

# Initialise the HoneyGain object
user = IPRoyalPawns()

# Optionally, when instantiating you can pass in the following attributes to the IPRoyalPawns class:
```

| Attribute      | Description        | Default Value                   |
|----------------|--------------------|---------------------------------|
| API_BASE_URL | The API BASE URL | https://pawns.iproyal.com                            |

```PYTHON
# Call the login method
user.login(USERNAME, PASSWORD)
```

---

### Add proxies for future requests:

```PYTHON
from pyIPRoyalPawns import IPRoyalPawns

# With authentication
user.set_proxy("ip:port:username:password")

# Without authentication
user.set_proxy("ip:port")
```

## Functions

---

1. Get user dashboard

    ```PYTHON
    user.dashboard()
    ```
---

2. Remove a proxy

    ```PYTHON
    # Removes a proxy for future requests.
    user.remove_proxy()
    ```
---

## Exceptions

- The following exceptions are defined.
    Exception | Reason
    --- | ---
    `NotLoggedInError` | Raised when you try to access protected routes (dashboard, payout history, etc).
    `HTMLWebpageParserError` | Raised when the webpage parser cannot parse the response of the dashboard request (typically when you're rate limited or a broken connection)

---

## Liked my work?

---

Consider donating:

- BTC: bc1q5y8z0cpgvafedvmwcfjn682skpr67e2du00acy

- LTC: LcquWHprnVRHY86u5rNDW6U8VD3WVbZV4h

