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
    return target in db.getAttackable(origin)

def validateSupport(origin, target, supporting):
    return target in db.getAttackableInCommon(origin, supporting)

def validateMove(origin, target):
    return target in db.getMoveable(origin)

def validateDefend(origin, target):
    return target in db.getDefendable(origin)