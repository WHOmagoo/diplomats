from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import diplomacyserver.gameEngine
import diplomacyserver.OrderValidator


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
            origin = content['origin']
            target = content['target']
            assisting = None

            if action == 'support':
                assisting = content['supporting']
                assisting = diplomacyserver.gameEngine.unitNameToId[assisting]

            origin = diplomacyserver.gameEngine.unitNameToId[origin]
            target = diplomacyserver.gameEngine.locationNameToId[target]
            action = diplomacyserver.gameEngine.ordertypes[action]

            valid = diplomacyserver.gameEngine.validateOrder(origin, action, target, assisting)

        except KeyError:
            print("Key error")
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


        return 200
    else:
        return 418


@app.route(defUrl + 'get_game', methods=['GET'])
def getGame():
    data = diplomacyserver.gameEngine.getGame()
    # data = getGame()

    out = []
    for team in data:
        out.append({"army": team[0], "navy": team[1], "score": team[2], "name": team[3]})

    return jsonify({"teams": out, "status":200})

@app.route(defUrl + 'get_targetable', methods=['POST'])
def getTargetable():
    if request.is_json:
        try:
            data = request.get_json()

            origin = data['origin']
            type = data['type']

            origin = diplomacyserver.gameEngine.unitNameToId[origin]
            type = diplomacyserver.gameEngine.ordertypes[type]

            targetableNames = diplomacyserver.OrderValidator.getTargetable(origin, type)
            targetable = []


            for target in targetableNames:
                targetable.append(diplomacyserver.gameEngine.locationIdToName[target])

            return jsonify({'status':200, 'targetable':targetable})

        except KeyError:
            print("Key error")
            return jsonify({"status":200,"targetable":[]})

        return jsonify({"status":200})
    else:
        return jsonify({"status":418})

@app.route(defUrl + 'get_attackable_in_common', methods=['POST'])
def getAttackableInCommon():
    if request.is_json:
        try:
            data = request.get_json()

            origin = data["origin"]
            supporting = data["supporting"]


            origin = diplomacyserver.gameEngine.unitNameToId[origin]
            supporting = diplomacyserver.gameEngine.unitNameToId[supporting]

            targetableNames = getAttackableInCommon(origin, supporting)
            targetable = []



            for target in targetableNames:
                targetable.append(diplomacyserver.gameEngine.locationIdToName[target])

            return jsonify({'status':200, 'targetable':targetable})
        except KeyError:
            print("Key error")
            return jsonify({"status":200, "targetable":[]})
    else:
        return jsonify({"status":418})

@app.route(defUrl + 'resolve_orders', methods=['GET'])
def resolveOrders():
    diplomacyserver.gameEngine.resolveOrders()

    data = diplomacyserver.gameEngine.getGame()

    out = []
    for team in data:
        out.append({"army": team[0], "navy": team[1], "score": team[2], "name": team[3]})

    return jsonify({"teams": out, "status":200})



if __name__ == '__main__':
    diplomacyserver.gameEngine.createGame()
    app.run()