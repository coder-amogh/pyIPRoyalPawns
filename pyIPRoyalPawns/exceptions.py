class IPRoyalPawnsAPIError(Exception):
	"""Base IPRoyalPawns API Exception."""
	def __init__(self, *args: object) -> None:
		super().__init__(*args)

class NotLoggedInError(IPRoyalPawnsAPIError):
	"""Raised when you're not logged in and try to access protected endpoints."""
	def __init__(self, *args: object) -> None:
		super().__init__(*args)

class AlreadyLoggedInError(IPRoyalPawnsAPIError):
	"""Raised when you're not logged in and try to access protected endpoints."""
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
