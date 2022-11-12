from pyIPRoyalPawns import IPRoyalPawns

from pprint import pprint

EMAIL, PASSWORD = ("email@example.com", "yourstrongpassword",)

user = IPRoyalPawns()

result = user.login(EMAIL, PASSWORD)

if result["success"]:
	print(user)

	# Get the dashboard information

	devices = user.devices()

	if devices["success"]:
		pprint(devices["json"])

	balance = user.balance()

	if balance["success"]:
		pprint(balance["json"])
else:
	print("Failed to logged in!")
	print("Status code:", result["response"].status_code)
