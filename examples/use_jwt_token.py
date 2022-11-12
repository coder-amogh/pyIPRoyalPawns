from pyIPRoyalPawns import IPRoyalPawns

EMAIL, PASSWORD = ("email@example.com", "yourstrongpassword",)

user = IPRoyalPawns()

login_result = user.login(EMAIL, PASSWORD)

if login_result["success"]:
	print(user)
	print("Am I logged in?", user.is_logged_in())
