from pyIPRoyalPawns import IPRoyalPawns

from pprint import pprint

TOKEN = "eyJtoken.jwtpawnsapp.iproyalpawns"

user = IPRoyalPawns()

user.set_jwt_token(TOKEN)

balance = user.balance()

pprint(balance)

