from rasa_nlu.model import Interpreter
import json
interpreter = Interpreter.load("./models/current/nlu")
message = "what is the next day for garbage collection?"
result = interpreter.parse(message)
print(json.dumps(result, indent=2))

intent = result["intent"]["name"]
entitieslist = result["entities"]

if intent == "trash_info":
    if result["entities"]:
        print("Got Entity:", entitieslist[0]["value"])
    else:
        print("No Entities")
print(intent)


