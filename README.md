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

# Initialise the IPRoyalPawns object
user = IPRoyalPawns()

# Optionally, when instantiating you can pass in the following attributes to the IPRoyalPawns class:
```

| Attribute      | Description        | Default Value                   |
|----------------|--------------------|---------------------------------|
| API_BASE_URL | The API BASE URL | https://api.pawns.app                            |
| API_PREFIX | The API PREFIX | /api                            |
| API_VERSION | The API VERSION | /v1                            |

```PYTHON
# Call the complete_login_flow method to login and set the JWT in self.jwt
user.complete_login_flow(USERNAME, PASSWORD)
```

---

### Add proxies for future requests:

```PYTHON
from pyIPRoyalPawns import IPRoyalPawns

# With authentication & protocol
user.set_proxy("ip:port:username:password", "socks5")

# Without authentication & protocol
user.set_proxy("ip:port", "socks5")

# Alternative way
user.set_socks5_proxy("ip:port")
user.set_socks5_proxy("ip:port:username:password")
user.set_https_proxy("ip:port")
user.set_https_proxy("ip:port:username:password")
```

## Functions

---

1. Get user balance

    ```PYTHON
    # Get balance and traffic sold as shown on the dashboard.
    user.balance()
    ```
---

2. Remove a proxy

    ```PYTHON
    # Removes a proxy for future requests.
    user.remove_proxy()
    ```
---

3. Get all the devices

    ```PYTHON
    # Get all the devices
    user.devices()
    ```
---

4. Payout history

    ```PYTHON
    # Get payout history
    user.payout_history()
    ```
---

5. Is Logged In

    ```PYTHON
    # Check if you're logged in
    user.is_logged_in()
    ```
---

6. Logout

    ```PYTHON
    # Logged out
    user.logout()
    ```
---

7. Set JWT Token

    ```PYTHON
    # Set JWT Token if you have one (otherwise use the login())
    user.set_jwt_token(TOKEN)
    ```
---

## Exceptions

- The following exceptions are defined.
    Exception | Reason
    --- | ---
    `NotLoggedInError` | Raised when you try to access protected routes (dashboard, payout history, etc).
    `AlreadyLoggedInError` | Raised when you try to login when you're already logged in.
---

## Liked my work?

---

Consider donating:

- BTC: bc1q5y8z0cpgvafedvmwcfjn682skpr67e2du00acy

- LTC: LcquWHprnVRHY86u5rNDW6U8VD3WVbZV4h

