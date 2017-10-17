from flask import Flask
from flask import request
import json

app = Flask(__name__)

defUrl = '/api/'

#recives and validates order
#order is of the form JSON: {“unitID”= int,”targetName”=string, “orderType”=string }
@app.route(defUrl + 'send_order', methods=['POST'])
def send_order():
    if request.is_json:
        #content will contain a dictionary describing the order
        content = request.get_json()
        #validate_order will return true if the order is valid
        #valid = validate_order(content)
        if valid:
            #order is ok
            return 200
        else:
            #order is not ok
            return 418
    else:
        return 418

#recives a faction name in a json and returns 200 when all other players
#have confirmed orders
#json of the form {"faction"="faction_name"}
@app.route(defUrl + 'confirm_orders', methods=['POST'])
def confirm_orders():
    if request.is_json:
        content = request.get_json()
        #waits until all orders are in then returns
        #confirm(content)
        return 200
    else:
        return 418
