from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from diplomacyserver import init


app = Flask(__name__)

defUrl = '/api/'

app = Flask(__name__)
CORS(app)

# recives and validates order
# order is of the form JSON: {“unitID”= int,”targetName”=string, “orderType”=string }

@app.route(defUrl + 'send_order', methods=['POST'])
def send_order():
    if request.is_json:
        # content will contain a dictionary describing the order
        content = request.get_json()

        try:
            action = content['action']
            origin = content['select']
            target = content['target']
            assisting = None

            if action == 'support':
                assisting = content['attack']
                assisting = init.locationNameToId[assisting]

            origin = init.unitNameToId[origin]
            target = init.locationNameToId[target]
            action = init.ordertypes[action]

            valid = init.validateOrder(origin, action, target, assisting)

        except KeyError:
            valid = False

        # validate_order will return true if the order is valid
        # valid = validate_order(content)
        if valid:
            #order is ok
            return jsonify({"status":200})
        else:
            #order is not ok
            return jsonify({"status":418})
    else:
        return jsonify({"status":418})

# recives a faction name in a json and returns 200 when all other players
# have confirmed orders
# json of the form {"faction"="faction_name"}


@app.route(defUrl + 'confirm_orders', methods=['POST'])
def confirm_orders():
    if request.is_json:
        content = request.get_json()
        # waits until all orders are in then returns
        # confirm(content)
        return 200
    else:
        return 418


@app.route(defUrl + 'get_game', methods=['GET'])
def getGame():
    data = init.getGame()

    out = []
    for team in data:
        temp = json.dumps(team[0])
        out.append({"army": team[0], "navy": team[1], "score": team[2], "name": team[3]})

    # return jsonify({"teams":[{"army": ["Portugal", "Ireland"], "navy":["Atlantic Ocean"], "score":3},
    # {"army": ["Portugal", "Ireland"], "navy":["Atlantic Ocean"], "score":2}], 'status':200})
    return jsonify({"teams": out, "status":200})

if __name__ == '__main__':
    init.createGame()
    app.run()