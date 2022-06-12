from bs4 import BeautifulSoup as BS

import requests

import pickle

from .exceptions import *

class IPRoyalPawnsHTMLWebpageParser:
	@classmethod
	def login(cls, response) -> dict:
		"""Parses the login page and returns the required payload"""
		payload = {}

		soup = BS(response.text, "lxml")

		input_token_el = soup.find("input", {
			"type": "hidden",
			"name": "_token",
		})

		token = input_token_el.get("value")

		payload["token"] = token

		return payload

	@classmethod
	def home(cls, response) -> dict:
		"""Parses the home page of the dashboard and returns the required payload"""

		payload = {}

		soup = BS(response.text, "lxml")

		try:
			balance_traffic_section = soup.select_one("section.ipr-card.payment_card")

			balance = balance_traffic_section.select_one(".payment_card__amount")

			# Balance
			payload["balance"] = balance.text.strip()

			traffic = balance_traffic_section.select_one(".payment_card__traffic")

			# Traffic
			payload["traffic"] = traffic.text.strip()

			devices_section = soup.select_one("section.active_devices_card")

			devices_list = devices_section.select_one("ul.active_devices__list")

			devices = devices_list.select("li.active_devices__item.active_devices__list-item")
			
			payload_devices = []

			for device in devices:
				device_info = {}

				device_info["ip"] = device.select_one("div").text.strip()
				device_info["platform"] = device.select_one("img.active_devices__platform").get("title").title()
				device_info["country"] = device.select_one("i.active_devices__flag-icon").get("title").upper()

				payload_devices.append(device_info)

			# Devices
			payload["devices"] = payload_devices

			try:
				referral_link = soup.select_one("input.aff_card__text-field.js-ref-url-aff-card").get("value")

				payload["referral_link"] = referral_link

			except:
				# Ignore the unimportant parser failures and continue
				pass

		except:
			raise HTMLWebpageParserError

		return payload

class IPRoyalPawns:
	def __init__(self, API_BASE_URL = "https://pawns.iproyal.com") -> None:
		"""Initialises IPRoyalPawns class"""
		self.API_BASE_URL = API_BASE_URL
		self.empty_session()
		self.remove_proxy()

	def save_session(self, filepath = "session.pkl") -> bool:
		"""Saves the IPRoyal session into a file"""
		with open(filepath, "wb") as f:
			pickle.dump(self._session, f)

		return True

	def load_session(self, filepath = "session.pkl") -> bool:
		"""Loads the IPRoyal session from a file"""
		with open(filepath, "rb") as f:
			self._session = pickle.load(f)

		return True

	def empty_session(self) -> bool:
		"""Empties the session"""
		self._session = requests.Session()
		return True

	def __make_request(self, req_type: str, endpoint: str, headers: dict = {}, *args, **kwargs):
		"""Helper function to make requests. """

		return self._session.request(req_type, f'{self.API_BASE_URL}{endpoint}', proxies = self.proxy_conf, headers = headers, *args, **kwargs)

	def set_proxy(self, proxy_str: str = None) -> bool:
		"""Sets the proxy for future API requests."""
		proxy = proxy_str.split(":")

		if len(proxy) > 2:
			ip, port, username, password = proxy

			self.proxy_conf = {
				"http": f"socks5://{username}:{password}@{ip}:{port}",
				"https": f"socks5://{username}:{password}@{ip}:{port}",
			}
		else:
			ip, port = proxy

			self.proxy_conf = {
				"http": f"socks5://{ip}:{port}",
				"https": f"socks5://{ip}:{port}",
			}

		return True

	def remove_proxy(self) -> bool:
		"""Removes the proxy for future API requests."""
		self.proxy_conf = None
		return True

	def __prepare_login(self) -> bool:
		"""Prepares login"""

		# Empty the session
		self.empty_session()

		# Call homepage to get the CSRF token and return response
		response = self.__make_request("GET", "/")

		if not response.ok:
			raise IPRoyalPawnsAPIError

		return response

	def login(self, email: str, password: str) -> bool:
		"""Logs in into the IPRoyalPawns dashboard"""

		prepared_login_response = self.__prepare_login()

		login_parsed_payload = IPRoyalPawnsHTMLWebpageParser.login(prepared_login_response)

		token = login_parsed_payload["token"]

		response = self.__make_request("POST", "/login", data = {
			"_token": token,
			"email": email,
			"password": password
		}, allow_redirects = True)

		return response.ok

	def dashboard(self) -> dict:
		"""Returns information shown on the main page of the dashboard"""

		response = self.__make_request("GET", "/", allow_redirects = False)

		if not response.ok:
			return NotLoggedInError

		home_parsed_payload = IPRoyalPawnsHTMLWebpageParser.home(response)

		return home_parsed_payload

	def __repr__(self):
		"""Represents the IPRoyalPawns object"""
		return f"<IPRoyalPawns object at {hex(id(self))}>"
