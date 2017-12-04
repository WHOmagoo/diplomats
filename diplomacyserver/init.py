from dbUtil import DB
import csv
import datetime



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
    factionIdDict = {}

    for faction in factions[0]:
        factionIdDict[faction] = db.makeFaction(faction, gameId)

    return factionIdDict


# Reads the location data from locations.csv and adds them to the database
# Returns a dictionary that converts location names to ids
def generateLocationDict(factionsDict):
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

        locID = db.makeLocation(0, 0, is_poi, type_id, factionsDict['None'])
        locationIdDict[name] = locID

    return locationIdDict


# Generates the neighbors and adds them to the database, only the smaller id is added to save space and time
def generateNeighbors(locationDict):
    db = DB()
    neighbors = parsecsv('neighbors.csv')

    for row in neighbors:
        currentLoc = row.pop(0)
        for loc in row:
            ida = locationDict[currentLoc]
            idb = locationDict[loc]

            if ida < idb:
                db.makeNeighbors(ida,idb)


def generateUnits(factionIdDict, locationIdLookup):
    db = DB()
    units = parsecsv('units.csv')
    unitIds = []

    for unit in units:
        name = unit[0]
        isnaval = unit[1]
        faction = unit[2]
        if isnaval == 'navy':
            isnaval = True
        elif isnaval == 'army':
            isnaval = False
        else:
            print("There was an error with unit isnaval " + name + ', ' + isnaval)
            break;

        if faction in factionIdDict.keys():
            faction = factionIdDict[faction]
        else:
            break;

        if name in locationIdLookup.keys():
            name = locationIdLookup[name]
        else:
            print("There was an error with unit name: %s" % name)

        unitIds.append(db.makeUnit(isnaval, name, faction));

    return unitIds;


if __name__ == '__main__':
    start = datetime.datetime.now()
    db = DB()

    gameId = db.makeGame()

    factionIdDict = generateFactionDict(gameId)
    locationIdDict = generateLocationDict(factionIdDict)
    print(locationIdDict)
    generateNeighbors(locationIdDict)
    unitIds = generateUnits(factionIdDict, locationIdDict)

    print("Initilized a game with id %s" % gameId)

    end = datetime.datetime.now()

    print("it took " + str(end - start))

    # for unit in unitids:
    #     db.removeUnit(unit)
    #
    # for name, locid in locationidlookup.items():
    #     db.removeNeighbors(locid)
    #
    # for name, locid in locationidlookup.items():
    #     db.removeLocation(locid)
    #
    # for f in factionidlookup.keys():
    #     db.removeFaction(factionidlookup[f])
    #
    # db.removeFaction(factionid)
    # db.removePlayer(playerid)
    # db.removeGame(gameid)

    # db.removeGameComponents(gameid)
