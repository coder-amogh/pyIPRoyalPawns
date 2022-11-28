from pyIPRoyalPawns import IPRoyalPawns

EMAIL, PASSWORD = ("email@example.com", "yourstrongpassword",)

user = IPRoyalPawns()

login_result = user.complete_login_flow(EMAIL, PASSWORD)

if login_result:
	print(user)
	print("Am I logged in?", user.is_logged_in())
