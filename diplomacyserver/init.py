from dbUtil import DB
import csv



def parsecsv(fileName):
    data = []
    with open(fileName) as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            data.append([])
            for col in row:
                data[-1:][0].append(col)

    return data


if __name__ == '__main__':
    db = DB()

    gameid = db.makeGame()
    playerid = db.makePlayer('none', 'none')
    factionid = db.makeFaction('none', gameid)

    factions = parsecsv('factions.csv')
    factionidlookup = {}

    for faction in factions[0]:
        factionidlookup[faction] = db.makeFaction(faction, gameid)

    locations = parsecsv('locations.csv')

    locationidlookup = {}
    unitids = []

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

        locID = db.makeLocation(0, 0, is_poi, type_id, factionid)
        locationidlookup[name] = locID
        # locationIDs[name] = locID

    print(locationidlookup)

    units = parsecsv('units.csv')

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

        if faction in factionidlookup.keys():
            faction = factionidlookup[faction]
        else:
            break;

        if name in locationidlookup.keys():
            name = locationidlookup[name]
        else:
            print("There was an error with unit name: %s" % name)

        unitids.append(db.makeUnit(isnaval, name, faction));

    print("Initilized a game with id %s" % gameid)

    for unit in unitids:
        db.removeUnit(unit)

    for name in locationidlookup.keys():
        db.removeLocation(locationidlookup[name])

    for f in factionidlookup.keys():
        db.removeFaction(factionidlookup[f])

    db.removeFaction(factionid)
    db.removePlayer(playerid)
    db.removeGame(gameid)

    # db.removeGameComponents(gameid)
