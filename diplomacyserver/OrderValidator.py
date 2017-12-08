from diplomacyserver.dbUtil import DB

db = DB()


def getAttackable(origin):
    return trimTuples(db.getAttackable(origin))

def getAttackableInCommon(origin, supporting):
    return trimTuples(db.getAttackableInCommon(origin, supporting))

def getMoveable(origin):
    return trimTuples(db.getMoveable(origin))

def getDefendable(origin):
    return trimTuples(db.getDefendable(origin))

def getSupportable(origin):
    return trimTuples(db.getSupportable(origin))

def validateAttack(origin, target):
    result = db.getAttackable(origin)
    for el in result:
        if target == el[0]:
            return True

    return False

def validateSupport(origin, target, supporting):
    result = db.getAttackableInCommon(origin, supporting)
    for el in result:
        if target == el[0]:
            return True

    return False

def validateMove(origin, target):
    result =  db.getMoveable(origin)
    for el in result:
        if target == el[0]:
            return True

    return False

def validateDefend(origin, target):
    result = db.getDefendable(origin)
    for el in result:
        if target == el[0]:
            return True

    return False

def getTargetable(origin, orderType):
    if orderType == 1:
        return getAttackable(origin)
    elif orderType == 2:
        return getSupportable(origin)
    elif orderType == 3:
        return getDefendable(origin)
    elif orderType == 4:
        return getMoveable(origin)
    else:
        return []

# Truncates a each tuple in a list to only its first item
def trimTuples(tupleList):
    result = []
    for item in tupleList:
        result.append(item[0])

    return result
