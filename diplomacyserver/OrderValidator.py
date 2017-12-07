from diplomacyserver.dbUtil import DB

db = DB()


def getAttackable(origin):
    return db.getAttackable(origin)

def getAttackableInCommon(origin, supporting):
    return db.getAttackableInCommon(origin, supporting)

def getMoveable(origin):
    return db.getMoveable(origin)

def getDefendable(origin):
    return db.getDefendable(origin)

def getSupportable(origin):
    return db.getSupportable(origin)

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