from garbage import getDates
from trash_binner import getBin
from rasa_nlu.model import Interpreter
import os
import json


from flask import Flask, request, redirect, render_template
from twilio.twiml.messaging_response import MessagingResponse

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

interpreter = Interpreter.load("./rasa/models/current/nlu")
app = Flask(__name__)

try:
    with open("address.db", "r") as db:
        dbString = db.read()
        dbJson = json.loads(dbString)
        myAddr = dbJson['current']
        #logger.info("current address is ==> {}".format(myAddr))
except:
    logger.error("couldn't load address, check address.db")


@app.route("/")
def welcome():
    return render_template("index.html", msg="msg from python")


@app.route("/processText", methods=['POST'])
def processText():
    """
    Primary function used for NLU
    """
    utterance = request.form['utterance']

    if utterance.lower().startswith('addr:'):
        address = utterance[5:]
        with open('address.db', 'w') as db:
            db.write(json.dumps({"current": address}))
        logger.info("Registered the new address successfully ==> %s" % address)
        return "Registered the new address successfully ==> %s" % address

    result = interpreter.parse(utterance)
    logger.info(json.dumps(result, indent=2))

    intent = result['intent']['name']
    entitieslist = result["entities"]

    if not entitieslist:
        entity = None
    else:
        entity = entitieslist[0]["value"]

    if intent == 'trash_info':
        if entity:
            returnString = getDates(entity)
        else:
            returnString = getDates()

    elif intent == 'bin_info':
        if entity is None:
            return "Can you rephrase that?"
        returnString = getBin(entity)

    elif intent == 'greet':
        returnString = "Hey, How can I help you!"

    elif intent == 'thankyou':
        returnString = "my pleasure."

    else:
        returnString = "Coudn't get that. Ask me about questions related to Trash Processing."

    return format_obj(returnString)


def format_obj(someObj):
    """
    Formating output into approprite HTML
    """

    if isinstance(someObj, dict):
        returnString = ''
        for key, val in someObj.items():
            returnString += '<b>' + key + '</b>'
            if isinstance(val, list):
                if isinstance(val[0], str):
                    returnString += toBullets(val)
            returnString += "<br>"
        return returnString

    elif isinstance(someObj, list):
        print('I am {} with type: {} and length: {}'.format(
            someObj, type(someObj), len(someObj)))
        if isinstance(someObj[0], list) and isinstance(someObj[0][0], bytes):
            # speical case handling, list of list with one bytes object and 1 string.
            return "<b>{} </b>should go to <b>{}</b>".format(someObj[0][0].decode(), someObj[0][1])
        return '<b>That would be</b>' + toBullets(someObj)

    return someObj


def toBullets(list_):
    """
    helper function to format_obj function
    """
    tempString = '<ul>'
    for i in list_:
        tempString += '<li>' + i + "</li>"
    tempString += '</ul>'

    logger.info(tempString)
    return tempString


@app.route('/talk')
def incoming_sms():
    """
    Function to be used with Twilio
    Test with sending POST requests from console

    Implement dictionary structure, with sucess, data, params etc

    """
    body = request.values.get('Body', None)

    if body is not None:
        body = body.lower().strip()

    returnString = processText(body)

    if isinstance(returnString, list):
        if isinstance(returnString[0], str):
            tempString = '\n\t'
            for i in returnString:
                tempString += ''.join(i) + "\n"
            returnString = tempString
        if isinstance(returnString[0], list):
            tempString = '\n\n'
            for i in returnString[:3]:
                tempString += i[0].decode() + " ==> " + i[1] + "\n"
            returnString = tempString

    resp = MessagingResponse()
    resp.message(returnString)
    return str(resp)


@app.route('/getInfo')
def getInfo():
    """
    function used for testing purposes
    """
    garbage_schedule = getDates()
    if garbage_schedule == 0:
        output_str = "Encounted a problem"

    else:
        output_str = ''
    for key, value in garbage_schedule.items():
        output_str += "{} --> {}\n".format(key, ", ".join(value))
    return output_str


def initiate_logger():
    import time
    import logging

    time_format = '%d-%b-%Y_%H-%M-%S'
    report_time = time.strftime(time_format)

    new_dir = 'server_logs'
    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)

    logging.basicConfig(
        format='%(asctime)s -- %(message)s',
        handlers=[logging.StreamHandler(),
                  logging.FileHandler('{}/debug_{}.log'.format(new_dir, report_time))],
        datefmt=time_format,
        level=logging.INFO,
    )

    """
    CRITICAL    50
    ERROR        40
    WARNING        30
    INFO        20
    DEBUG        10
    NOTSET        0
    """

    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

initiate_logger()

if __name__ == "__main__":
    app.run(debug=True)
