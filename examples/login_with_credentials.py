from pyIPRoyalPawns import IPRoyalPawns

EMAIL, PASSWORD = ("email@example.com", "yourstrongpassword",)

user = IPRoyalPawns()

if user.login(EMAIL, PASSWORD):
	print(user)
	print("Logged in!")
	print("User Session:", user._session)
