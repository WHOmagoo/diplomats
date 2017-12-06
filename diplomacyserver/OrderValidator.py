from dbUtil import DB

db = DB()

def validateAttack(origin, target):
    return target in db.getAttackable(origin)