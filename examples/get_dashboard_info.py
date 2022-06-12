from pyIPRoyalPawns import IPRoyalPawns

EMAIL, PASSWORD = ("email@example.com", "yourstrongpassword",)

user = IPRoyalPawns()

if user.login(EMAIL, PASSWORD):
	print(user)
	
	# Get the dashboard information

	dashboard = user.dashboard()

	print("Balance:", dashboard["balance"])
	print("Devices:", dashboard["devices"])
	print("Traffic:", dashboard["traffic"])
	print("Referral Link:", dashboard.get("referral_link", None))

