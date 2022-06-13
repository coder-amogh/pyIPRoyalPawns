from bs4 import BeautifulSoup as BS

import requests

import pickle

from .exceptions import *

class IPRoyalPawnsHTMLWebpageParser:
	@classmethod
	def login(cls, response) -> dict:
		"""Parses the login page and returns the required payload"""
		try:
			payload = {}

			soup = BS(response.text, "lxml")

			input_token_el = soup.find("input", {
				"type": "hidden",
				"name": "_token",
			})

			token = input_token_el.get("value")

			payload["token"] = token

		except:
			raise HTMLWebpageParserError

		return payload

	@classmethod
	def home(cls, response) -> dict:
		"""Parses the home page of the dashboard and returns the required payload"""
		payload = {}

		try:
			soup = BS(response.text, "lxml")
	
			balance_traffic_section = soup.select_one("section.ipr-card.payment_card")

			balance = balance_traffic_section.select_one(".payment_card__amount")

			# Balance
			payload["balance"] = balance.text.strip()

			traffic = balance_traffic_section.select_one(".payment_card__traffic")

			# Traffic
			payload["traffic"] = traffic.text.strip()

			# devices_section = soup.select_one("section.active_devices_card")

			# devices_list = devices_section.select_one("ul.active_devices__list")

			devices_list = soup.select_one("ul.active_devices__list")

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

	@classmethod
	def devices(cls, response) -> list:
		"""Parses devices information on a specific page and returns the required payload"""
		payload_devices = []

		try:
			soup = BS(response.text, "lxml")

			devices_list = soup.select_one("ul.active_devices__list")

			devices = devices_list.select("li.active_devices__item.active_devices__list-item")

			for device in devices:
				device_info = {}

				device_info["ip"] = device.select_one("div").text.strip()
				device_info["platform"] = device.select_one(
					"img.active_devices__platform").get("title").title()
				device_info["country"] = device.select_one(
					"i.active_devices__flag-icon").get("title").upper()

				payload_devices.append(device_info)
		except:
			raise HTMLWebpageParserError

		# Devices
		return payload_devices

	@classmethod
	def devices_pagination(cls, response) -> dict:
		"""Parses devices pagination information and returns the required payload"""	
		try:
			soup = BS(response.text, "lxml")

			pagination_ul = soup.select_one("ul.pagination")

			if pagination_ul is None:
				return {
					"previous": None,
					"first": None,
					"active": None,
					"next": None,
					"last": None,
				}

			active = int(pagination_ul.select_one("li.page-item.active").get_text().strip())

			first = int(pagination_ul.select("li.page-item")[1].get_text().strip())

			last = int(pagination_ul.select("li.page-item")[-2].get_text().strip())

			previous = None if active == 1 else active - 1

			next_ = None if last == active else active + 1

			return {
				"previous": previous,
				"first": first,
				"active": active,
				"next": next_,
				"last": last,
			}

		except:
			raise HTMLWebpageParserError

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

	def __handle_not_logged_in(self, response) -> None:
		if response.status_code == 302:
			raise NotLoggedInError

	def __handle_api_error(self, response) -> None:
		if not response.ok:
			raise IPRoyalPawnsAPIError

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

		self.__handle_not_logged_in(response)
		self.__handle_api_error(response)

		home_parsed_payload = IPRoyalPawnsHTMLWebpageParser.home(response)

		return home_parsed_payload

	def devices(self) -> dict:
		"""Returns all the devices information (the dashboard() only returns upto 5 devices)"""
		response = self.__make_request("GET", "/active-devices")

		self.__handle_not_logged_in(response)
		self.__handle_api_error(response)

		pagination = IPRoyalPawnsHTMLWebpageParser.devices_pagination(response)

		if pagination["first"] is None or pagination["last"] is None:
			raise HTMLWebpageParserError

		devices = []

		for page in range(pagination["first"], pagination["last"] + 1):
			response = self.__make_request("GET", f"/active-devices?page={page}")

			devices_page_parsed_payload = IPRoyalPawnsHTMLWebpageParser.devices(response)

			devices.extend(devices_page_parsed_payload)

		return devices

	def __repr__(self):
		"""Represents the IPRoyalPawns object"""
		return f"<IPRoyalPawns object at {hex(id(self))}>"
