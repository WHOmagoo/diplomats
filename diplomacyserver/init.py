from dbUtil import DB
import csv
import datetime


locationNameToId = {}
locationIdToName = {}
unitNameToId = {}
unitIdToName = {}
factionNameToId = {}
factionIdToName = {}

ordertypes = {'Attack':1, 'a':1, 'Support':2, 's':2, 'Defend':3, 'd':3, 'Move':4, 'm':4, 'Stay':5, 's':5}

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
    db = DB()
    factions = parsecsv('factions.csv')

    for faction in factions[0]:
        id = db.makeFaction(faction, gameId)
        factionNameToId[faction] = id
        factionIdToName[id] = faction


# Reads the location data from locations.csv and adds them to the database
# Returns a dictionary that converts location names to ids
def generateLocationDict():
    db = DB()
    locations = parsecsv('locations.csv')

    locationIdDict = {}

    for row in locations:
        name = row[0]
        type_id = row[1]
        is_poi = row[2]

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

        locID = db.makeLocation(0, 0, is_poi, type_id, factionNameToId['None'])
        locationNameToId[name] = locID
        locationIdToName[locID] = name

    # return locationIdDict


# Generates the neighbors and adds them to the database, only the smaller id is added to save space and time
def generateNeighbors():
    db = DB()
    neighbors = parsecsv('neighbors.csv')

    for row in neighbors:
        currentLoc = row.pop(0)
        for loc in row:
            ida = locationNameToId[currentLoc]
            idb = locationNameToId[loc]

            if ida < idb:
                db.makeNeighbors(ida,idb)

def generateUnits():
    db = DB()
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
    db = DB()

    gameId = db.makeGame()

    generateFactionDict(gameId)
    generateLocationDict()
    generateNeighbors()
    generateUnits()

def getAttackable(unitId):
    db = DB()
    unit = db.getUnit(unitId)
    neighbors = db.getNeighbors(unit[2])

    drop = []

    for loc in neighbors:
        if loc[5] == unit[4]:
            drop.append(loc)
        elif unit[1] and loc[4] == 1:
            drop.append(loc)
        elif not unit[1] and loc[4] == 3:
            drop.append(loc)

    for loc in drop:
        neighbors.remove(loc)

    print(neighbors)

def makeOrder(unitid, type, target):
    db = DB()
    locationOrigin = db.getUnitLocation(unitid)
    neighbors = getNeighbors(locationOrigin[3])

    if target in neighbors:
        order = db.makeUnitOrder(type, target)
        db.setOrder(unitid, order)
    else:
        print("Target is not in neighbors")

def resolveOrders():
    db = DB()
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
        origin = db.getOrigin(order[2])
        attackingId = order([2])

        db.updateUnitLocation(origin, attackingId)



    print(orders)



def getOrderType(name):
    id = 0
    try:
        id = ordertypes[name]
    except KeyError:
        pass

    return id

def getNeighbors(locationId):
    db = DB()
    neighbors = db.getNeighbors(locationId)
    result = []
    for e in neighbors:
        result.append(e[3])
    return result


def printLocations(locationList):
    result = ''
    for loc in locationList:
        result = result + locationIdToName[loc] + ', '

    print(result)




def removeGame(gameData):
    pass

if __name__ == '__main__':

    # result = input('Enter a command: ')
    # print(result)
    gameData = createGame()
    # locationDict = gameData[2]
    # unitDict = gameData[3]

    print("Welcome to web Diplomacy!")
    print("A note about the parameters, instead of using a space for loactions with a space in the name, use a dash")
    print("Commands enterable are: list, neighbors <location>, order <unitLocation> <orderType> <target>, confirm, exit")



    while True:
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
                    location = command[1].replace(',', ' ')
                    type = command[2]
                    target = command[3].replace(',', ' ')

                    location = unitNameToId[location]
                    type = ordertypes[type]
                    target = locationNameToId[target]

                    makeOrder(location, type, target)
                except KeyError:
                    print("One or more of the inputs was incorrect")
            elif command[0] == 'confirm':
                resolveOrders()
            else:
                print("Command not recognized")
        except IndexError:
            print("Wrong number of parameters for command " + command)


    # print(gameData)



    # getAttackable(gameData[3]["Kiel"])
