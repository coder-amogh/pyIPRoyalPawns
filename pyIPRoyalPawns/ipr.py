import requests
import random
import string

from .exceptions import *

class IPRoyalPawns:
	__LOGIN_TOKEN_LENGTH = 21

	def __init__(self, API_BASE_URL = "https://api.pawns.app", API_PREFIX = "/api", API_VERSION = "/v1") -> None:
		"""Initialises IPRoyalPawns class. """
		self.API_URL = API_BASE_URL + API_PREFIX + API_VERSION

		self.remove_all_headers()
		self.add_default_headers({
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
			"X-Locale": "EN",
		})

		self.remove_proxy()
		self.logout()

	def remove_all_headers(self) -> bool:
		"""Removes all default headers for future requests. """
		self.__headers = {}

	def add_default_headers(self, headers: dict = {}) -> bool:
		"""Adds default headers for future requests. Could be used to set user-agent for example. """
		self.__headers = {
			**self.__headers, **headers
		}

		return True

	def __return_response(self, response) -> dict:
		result = {}

		result["success"] = bool(response.ok)
		result["json"] = response.json()
		result["response"] = response

		return result

	def logout(self) -> bool:
		return self.set_jwt_token(None)

	def __make_request(self, req_type: str, endpoint: str, headers: dict = {}, *args, **kwargs):
		"""Helper function to make requests. """

		return requests.request(req_type, f'{self.API_URL}{endpoint}', proxies = self.proxy_conf, headers = {
            **self.__headers, **headers, **({
                "Authorization": f"Bearer {self.jwt}",
            } if self.is_logged_in() else {}),
        }, *args, **kwargs)

	def set_proxy(self, proxy_str: str = None, protocol: str = "socks5") -> bool:
		"""Sets the proxy for future API requests."""

		if proxy_str is None:
			self.proxy_conf = None
			return True

		proxy = proxy_str.split(":")

		if len(proxy) > 2:
			ip, port, username, password = proxy

			self.proxy_conf = {
				"http": f"{protocol}://{username}:{password}@{ip}:{port}",
				"https": f"{protocol}://{username}:{password}@{ip}:{port}",
			}
		else:
			ip, port = proxy

			self.proxy_conf = {
				"http": f"{protocol}://{ip}:{port}",
				"https": f"{protocol}://{ip}:{port}",
			}

		return True

	def set_socks5_proxy(self, proxy_str: str = None) -> bool:
		"""Sets SOCKS5 proxy for future API requests. """
		return self.set_proxy(proxy_str, "socks5")

	def set_http_proxy(self, proxy_str: str = None) -> bool:
		"""Sets HTTP proxy for future API requests. """
		return self.set_proxy(proxy_str, "http")

	def set_https_proxy(self, proxy_str: str = None) -> bool:
		"""Sets HTTPS proxy for future API requests. """
		return self.set_proxy(proxy_str, "https")

	def remove_proxy(self) -> bool:
		"""Removes the proxy for future API requests. """
		return self.set_proxy(None)

	def __handle_not_logged_in(self) -> None:
		if not self.is_logged_in():
			raise NotLoggedInError

	def __prepare_login(self) -> bool:
		"""Prepares login"""

		return {
			"token": self.__get_login_token(),
		}

	def __get_login_token(self) -> str:
		"""IPRoyalPawns needs a 21 characters (which include uppercase, lowercase and numbers) long as an ID/token. We generate it on the client-side and send it. """

		return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(IPRoyalPawns.__LOGIN_TOKEN_LENGTH))

	def is_logged_in(self) -> bool:
		"""Returns if we're logged in or not. """
		return self.jwt is not None

	def set_jwt_token(self, jwt: str = None) -> bool:
		"""Sets the JWT token for future requests. """
		self.jwt = jwt
		return True

	def login(self, email: str, password: str, h_captcha_response: str = "") -> dict:
		"""Logs in into the IPRoyalPawns dashboard. """

		if self.is_logged_in():
			raise AlreadyLoggedInError

		prepared_login_info = self.__prepare_login()

		token = prepared_login_info["token"]

		response = self.__make_request("POST", "/users/tokens", json = {
			"identifier": token,
			"email": email,
			"password": password,
			"h_captcha_response": h_captcha_response,
		})

		return self.__return_response(response)

	def complete_login_flow(self, email: str, password: str, h_captcha_response: str = "") -> bool:
		login_result = self.login(email, password, h_captcha_response)

		if login_result["success"]:
			token = login_result["json"]["access_token"]

			self.set_jwt_token(token)

			return True

		return False

	def me(self) -> dict:
		"""Returns information about the logged in user. """
		self.__handle_not_logged_in()

		response = self.__make_request("GET", "/users/me")

		return self.__return_response(response)

	def my_payout_data(self) -> dict:
		"""Returns information about the payout data for the logged in user. """
		self.__handle_not_logged_in()

		response = self.__make_request("GET", "/users/me/payout-data")

		return self.__return_response(response)

	def add_confirmation_code(self, action: str = "store_payout") -> dict:
		"""Adds confirmation code for an action. """
		self.__handle_not_logged_in()

		response = self.__make_request("POST", "/users/me/confirmation-codes", json = {
			"action": action,
		})

		return self.__return_response(response)

	def payout(self, method_id: int, code: str):
		"""Adds confirmation code for an action. """
		self.__handle_not_logged_in()

		response = self.__make_request("POST", "/users/me/payouts", json = {
			"payout_method_id": method_id,
		}, headers = {
			"X-Confirmation-Code": code
		})

		return self.__return_response(response)

	def cancel_payout(self):
		"""Cancels a pending payout. """
		self.__handle_not_logged_in()

		response = self.__make_request("POST", "/users/me/payouts/cancel")

		return self.__return_response(response)

	def devices(self, page: int = 1, items_per_page: int = 20) -> dict:
		"""Returns all the devices information. """
		self.__handle_not_logged_in()

		response = self.__make_request("GET", "/users/me/devices", params = {
			"page": page,
			"items_per_page": items_per_page,
		})

		return self.__return_response(response)

	def balance(self) -> dict:
		"""Returns balance information. """
		self.__handle_not_logged_in()

		response = self.__make_request("GET", "/users/me/balance")

		return self.__return_response(response)

	def payouts(self, page: int = 1) -> dict:
		"""Returns payouts information. """
		self.__handle_not_logged_in()

		response = self.__make_request("GET", "/users/me/payouts", params = {
			"page": page,
		})

		return self.__return_response(response)

	def affiliate_payouts(self, page: int = 1) -> dict:
		"""Returns affiliate payouts information. """
		self.__handle_not_logged_in()

		response = self.__make_request("GET", "/users/me/affiliate/payouts", params = {
			"page": page,
		})

		return self.__return_response(response)

	def countries(self) -> dict:
		"""Returns countries information. Used in payout_methods() for example. """

		response = self.__make_request("GET", "/countries")

		return self.__return_response(response)

	def payout_methods(self, country_id: int) -> dict:
		"""Returns payout methods available in your country. Use `countries()` to get the `country_id`. """

		response = self.__make_request("GET", f"/countries/{country_id}/payout-methods")

		return self.__return_response(response)
	
	def affiliate_stats(self) -> dict:
		"""Returns affiliate stats information. """
		self.__handle_not_logged_in()

		response = self.__make_request("GET", "/users/me/affiliate/stats")

		return self.__return_response(response)

	def __repr__(self):
		"""Represents the IPRoyalPawns object. """
		return f"<IPRoyalPawns object at {hex(id(self))}>"
