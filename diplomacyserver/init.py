import csv

from diplomacyserver import OrderValidator
from diplomacyserver.dbUtil import DB

locationNameToId = {}
locationIdToName = {}
unitNameToId = {}
unitIdToName = {}
factionNameToId = {}
factionIdToName = {}
db = DB()

ordertypes = {'Attack':1, 'a':1, 'Support':2, 's':2, 'Defend':3, 'd':3, 'Move':4, 'm':4, 'Stay':5, 's':5}

def getGame():
    return [(["Liverpool", "Ireland"], ["IrishSea"], 3), (["Casablanca"], ["AtlanticOcean"], 1)]

def parsecsv(fileName):
    data = []
    with open(fileName) as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            data.append([])
            for col in row:
                data[-1:][0].append(col)

    return data


# Reads the faction names from factions.csv and adds them to the database,
# Returns a dictionary that converts names to ids
def generateFactionDict(gameId):
    # db = DB()
    factions = parsecsv('factions.csv')

    for faction in factions[0]:
        id = db.makeFaction(faction, gameId)
        factionNameToId[faction] = id
        factionIdToName[id] = faction


# Reads the location data from locations.csv and adds them to the database
# Returns a dictionary that converts location names to ids
def generateLocationDict():
    # db = DB()
    locations = parsecsv('locations.csv')

    locationIdDict = {}

    for row in locations:
        name = row[0]
        xpos = row[1]
        ypos = row[2]
        type_id = row[3]
        is_poi = row[4]

        if is_poi == 'TRUE':
            is_poi = True
        elif is_poi == 'FALSE':
            is_poi = False
        else:
            print("There was an error, " + is_poi)
            break

        if type_id == 'landlocked':
            type_id = 1
        elif type_id == 'coastal':
            type_id = 2
        elif type_id == 'ocean':
            type_id = 3
        else:
            print("There was an error, " + type_id)
            break;

        locID = db.makeLocation(xpos, ypos, is_poi, type_id, factionNameToId['None'])
        locationNameToId[name] = locID
        locationIdToName[locID] = name

    # return locationIdDict


# Generates the neighbors and adds them to the database, only the smaller id is added to save space and time
def generateNeighbors():
    # db = DB()
    neighbors = parsecsv('neighbors.csv')

    for row in neighbors:
        currentLoc = row.pop(0)
        for loc in row:
            ida = locationNameToId[currentLoc]
            idb = locationNameToId[loc]

            if ida < idb:
                db.makeNeighbors(ida,idb)

def generateUnits():
    # db = DB()
    units = parsecsv('units.csv')
    unitIds = {}

    for unit in units:
        location = unit[0]
        isnaval = unit[1]
        faction = unit[2]

        if isnaval == 'navy':
            isnaval = True
        elif isnaval == 'army':
            isnaval = False
        else:
            print("There was an error with unit isnaval " + location + ', ' + isnaval)
            break;

        if faction in factionNameToId.keys():
            faction = factionNameToId[faction]
        else:
            print("There was an error with unit faction " + location)
            break;

        if location in locationNameToId.keys():
            location = locationNameToId[location]
        else:
            print("There was an error with unit name: %s" % location)
            break;

        id = (db.makeUnit(isnaval, location, faction))
        unitNameToId[unit[0]] = id
        unitIdToName[id] = unit[0]

def createGame():
    # db = DB()

    gameId = db.makeGame()

    generateFactionDict(gameId)
    generateLocationDict()
    generateNeighbors()
    generateUnits()

def makeOrder(unitid, type, target):
    # db = DB()
    locationOrigin = db.getUnitLocation(unitid)
    neighbors = getNeighbors(locationOrigin[3])

    if target in neighbors:
        order = db.makeUnitOrder(type, target)
        db.setOrder(unitid, order)
    else:
        print("Target is not in neighbors")

def resolveOrders():
    # db = DB()
    orders = []
    for unit, id in unitNameToId.items():
        order = db.getOrderData(id)
        if order is not None:
            orders.append(order)

    success = []
    for order in orders:
        if db.isEmpty(order[2]):
            success.append(order)

    for order in success:
        origin = db.getOrigin(order[0])
        attackingId = order[2]

        db.updateUnitLocation(origin, attackingId)


def getOrderType(name):
    id = 0
    try:
        id = ordertypes[name]
    except KeyError:
        pass

    return id

def getNeighbors(locationId):
    # db = DB()
    neighbors = db.getNeighborsFromLocation(locationId)
    result = []
    for e in neighbors:
        result.append(e[3])
    return result


def printLocations(locationList):
    result = ''
    for loc in locationList:
        result = result + locationIdToName[loc] + ', '

    print(result)

def resolveOrders2():
    undeterminedOrders = []
    actionableOrders = []
    orderAtLocation = {}
    for key, val in unitIdToName.items():
        order = db.getOrderData(key)
        undeterminedOrders.append(order)
        orderAtLocation[db.getUnitLocation(key)] = order

    undeterminedLastSize = 0
    while undeterminedLastSize != len(undeterminedOrders) or len(undeterminedOrders) == 0:
        buffer = []
        for order in undeterminedOrders:
            if order[1] == 1:
                try:
                    buffer.append(orderAtLocation[order[2]])
                except KeyError:
                    pass

        for order in undeterminedOrders:
            if order not in buffer:
                actionableOrders.append(order)

        undeterminedLastSize = len(undeterminedOrders)
        undeterminedOrders = buffer

        print("Total Length:" + str(len(actionableOrders) + len(undeterminedOrders)) +
              ", Actionable Orders Length:" + str(len(actionableOrders)) +
              ', Undetermined Orders Length:' + str(len(undeterminedOrders)))


    attacks = []
    supports = []
    defenses = []
    moves = []
    stay = []

    locationIdToAttacking = {}

    for order in actionableOrders:
        if order[1] == 1:
            attacks.append((order, 1))
        if order[1] == 2:
            supports.append(order)
        if order[1] == 3:
            defenses.append(order)
        if order[1] == 4:
            moves.append(order)
        if order[1] == 5:
            stay.append(order)

    locationIdToAttackStrength = {}

    for attack in attacks:
        originLocation = db.getOrigin(attack[0])
        locationIdToAttacking[originLocation] = attack[2]
        locationIdToAttackStrength[originLocation] = 1

    for support in supports:
        try:
            if support[2] == locationIdToAttacking[3]:
                locationIdToAttacking[support[2]] += 1
        except KeyError:
            pass

    locationToDefenseStrength = {}

    for id, name in unitIdToName:
        locationToDefenseStrength[db.getUnitLocation(id)] = 1;

    for defense in defenses:
        locationToDefenseStrength[defense[2]] += 1

    successfullAttacks = {}

    for location, attacking in locationIdToAttacking:
        if locationIdToAttackStrength[location] > locationToDefenseStrength[location]:
            if attacking in successfullAttacks.items():
                successfullAttacks[attacking].append((location, locationIdToAttackStrength[location]))
            else:
                successfullAttacks[attacking] = [(location, locationIdToAttackStrength[location])]

    strongestAttacks = []

    for location, attacksOnLocation in successfullAttacks.items():
        bestAttackStrength = 0
        attacksWithStrength = []
        for attack in attacksOnLocation:
            if attack[0] > bestAttackStrength:
                bestAttackStrength = attack[0]
                attacksWithStrength = [attack]
            elif attack[0] == bestAttackStrength:
                attacksWithStrength.append(attack)

        if len(attacksWithStrength) == 1:
            strongestAttacks.append(attacksWithStrength[0])





# 1 Attack
# 2 Support
# 3 Defend
# 4 MoveOrder
# 5 Stay


def updateGame():
    unitNameToId.clear()
    unitIdToName.clear()
    for key, value in locationIdToName.items():
        unit = db.getUnit(key)
        if unit is not None:
            unitNameToId[value] = unit[0]
            unitIdToName[unit[0]] = value

    print(unitNameToId)



def removeGame(gameData):
    pass

def game():

    # result = input('Enter a command: ')
    # print(result)
    gameData = createGame()
    updateGame()
    # locationDict = gameData[2]
    # unitDict = gameData[3]

    print("Welcome to web Diplomacy!")
    print("A note about the parameters, instead of using a space for loactions with a space in the name, use a dash")
    print("Commands enterable are: list, neighbors <location>, order <unitLocation> <orderType> <target>, confirm, exit")



    while False:
        command = input('Command: ')
        command = command.split(" ", 3)

        try:
            if command[0] == 'list' or command[0] == 'l':
                print(unitNameToId)
            elif command[0] == 'neighbors' or command[0] == 'n':
                try:
                    printLocations(getNeighbors(locationNameToId[command[1]]))
                except KeyError:
                    print(command[1] + " is not a location")
            elif command[0] == 'exit':
                break;
            elif command[0] == 'order' or command[0] == 'o':
                try:
                    origin = command[1].replace(',', ' ')
                    type = command[2]
                    target = command[3].replace(',', ' ')


                    origin = unitNameToId[origin]
                    type = ordertypes[type]
                    target = locationNameToId[target]

                    makeOrder(origin, type, target)
                except KeyError:
                    print("One or more of the inputs was incorrect")
            elif command[0] == 'a':
                origin = command[1].replace(',', ' ')
                origin = unitNameToId[origin]
                attackable = OrderValidator.getAttackable(origin)
                for id in attackable:
                    print(locationIdToName[id[0]] + ", ", end="")

                print()

            elif command[0] == 'd':
                origin = command[1].replace(',', ' ')
                origin = unitNameToId[origin]
                for id in OrderValidator.getDefendable(origin):
                    print(locationIdToName[id[0]] + ", ", end="")

                print()
            elif command[0] == 's':
                origin = command[1].replace(',', ' ')
                origin = unitNameToId[origin]
                for id in OrderValidator.getSupportable(origin):
                    print(locationIdToName[id[0]] + ", ", end="")

                print()
                pass
            elif command[0] == 'm':
                origin = command[1].replace(',', ' ')
                origin = unitNameToId[origin]
                for id in OrderValidator.getMoveable(origin):
                    print(locationIdToName[id[0]] + ", ", end="")

                print()
                pass
            elif command[0] == 'aic':
                origin = command[1].replace(',', ' ')
                origin = unitNameToId[origin]
                secondary = command[2].replace(',', ' ')
                secondary = unitNameToId[secondary]
                for id in OrderValidator.getAttackableInCommon(origin, secondary):
                    print(locationIdToName[id[0]] + ", ", end="")

                print()
                pass
            elif command[0] == 'confirm':
                resolveOrders()
                updateGame()
            else:
                print("Command not recognized")

        except IndexError:
            print("Wrong number of parameters for command " + str(command))
        except KeyError:
            print("Something was misspelled in "  + str(command))


    # print(gameData)



    # getAttackable(gameData[3]["Kiel"])
