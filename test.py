import json

with open("address.db", "r") as db:
	dbString = db.read()
	dbJson = json.loads(dbString)
	myAddr = dbJson['current']
	print(f'current address is {myAddr}')

utterance = "addr: 125220 daffodil place, brampton"
if utterance.startswith('addr:'):
	address = utterance[5: ]
	with open('address.db', 'w') as db:
		db.write(json.dumps({"current": address}, ))
	print( "Registered the new address successfully")
