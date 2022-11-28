from pyIPRoyalPawns import IPRoyalPawns

EMAIL, PASSWORD = ("email@example.com", "yourstrongpassword",)

user = IPRoyalPawns()

login_result = user.complete_login_flow(EMAIL, PASSWORD)

if login_result:
	# Requests a confirmation code to your email
	user.add_confirmation_code()

	# You can payout with something like this:
	# user.payout(method_id = 1, code = "696969")
	# method_id = 1 = BTC payout method, code = 696969 = the code which will be sent to your email

	# In real-life, you could ask the code to the user using the built-in input() method:

	code = input("Enter the code sent to your email:")

	result = user.payout(method_id = 1, code = code)

	if result["success"]:
		print("Payout created!", result["json"])
