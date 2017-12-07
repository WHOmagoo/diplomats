#used to help with order resolution
class const:
    #The first three are to be used while resolving orders
    NOT_AFFECTED = 0
    INDETERMINATE = 1
    EXECUTABLE = 2
    CANCELED = 3

    #Should be used
    SUCCEEDED = 3
    FAILED = 4

    #Order Types
    ATTACK = 5
    SUPPORT = 6
    DEFEND = 7
    MOVE = 8

# Parameters: a list of units with valid orders
def resolveOrders(units):
    #A hash of all the orders
    # key = location, val = order
    ordersHash = {}

    executedOrders = []

    #A has of all the successful attack orders
    #key = order, val = int power
    attackPowers = {}

    #A hash of all the places that had at least one successful attack
    #key = location, val = list of orders
    placesFailedToDefend = {}

    #A hash of all of the defensive powers
    #key = location, val = int power
    defensePowers = {}

    #A list of all orders that were not canceled
    executableOrdersList = []

    for unit in units:
        ordersHash[unit] = (unit.getCurOrder(), const.NOT_AFFECTED)

    while len(ordersHash) > 0:

        for unit in units:
            if unit.getCurOrder().getOrderType() == const.ATTACK:
                target = unit.getCurOrder().getTarget().getUnit()
                ordersHash[target] = (target, const.INDETERMINATE)

        for unit in units:
            if unit[1] == const.NOT_AFFECTED:
                executableOrdersList.append(unit)
                ordersHash.pop(unit)
                ordersHash.pop(unit.getCurOrder.getTarget().getUnit())

    for unit in executableOrdersList:
        thisOrder = unit.getCurOrder()
        if thisOrder.getOrderType() == const.ATTACK:
            attackPowers[thisOrder] = 1;

    for unit in executableOrdersList:
        thisOrder = unit.getCurOrder()
        if thisOrder.getOrderType() == const.SUPPORT and thisOrder.getSupporting() in attackPowers:
            attackPowers[thisOrder.getSupporting()] += 1

    for unit in executableOrdersList:
        thisOrder = unit.getCurOrder();
        if thisOrder.getOrderType() == const.DEFEND:
            if thisOrder.getTarget() in defensePowers:
                defensePowers[thisOrder.getTarget()] += 1
            else:
                defensePowers[thisOrder.getTarget()] = 2

    for attack in attackPowers:
        if attack.getTarget() in defensePowers and attackPowers[attack] < defensePowers[attack.getTarget()]:
            if attack.getTarget() in placesFailedToDefend:
                placesFailedToDefend[attack.getTarget()].append(attack)
            else:
                placesFailedToDefend[attack.getTarget()] = [attack]

            #checks for multiple units attacking the same territory. Will bounce units if there is not a single attack that is the strongest
    for territory in placesFailedToDefend:
        max_attack_value = 0
        for attack in placesFailedToDefend[territory]:
            if attackPowers[attack] > max_attack_value:
                max_attack_value = attackPowers[attack]
            elif attackPowers[attack] < max_attack_value:
                attackPowers.pop(attack)

        for attack in placesFailedToDefend[territory]:
            if attackPowers[attack] < max_attack_value:
                attackPowers.pop(attack)

        if len(attackPowers.keys()) != 1:
            placesFailedToDefend[territory].clear()
        else:
            for attack in placesFailedToDefend[territory]:
                executedOrders.append(attack)

    for attack in executedOrders:
        attack.getTarget().setOccupiedBy(attack.getUnit())

    for unit in executableOrdersList:
        if unit.getCurOrder().getType == const.MOVE and unit.getCurOrder().getAffect().isOcuppied() == False:
            executedOrders.append(unit.getCurOrder())