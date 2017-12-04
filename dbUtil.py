import psycopg2

'''
Used to make DB a singleton
'''
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DB(metaclass=Singleton):
    def __init__(self):
        self.conn = psycopg2.connect("dbname=diplomacy user=postgres password=password host=localhost")
        self.cur = self.conn.cursor()
        self.conn.commit()
        print("Initialized DB")

    def __del__(self):
        self.cur.close()
        self.conn.close()

    """ ============ CONSTRUCTORS ========== """

    def makeGame(self):
        self.cur.execute("INSERT INTO diplomacy.game default values;")
        self.conn.commit()
        self.cur.execute("SELECT max(gameid) FROM diplomacy.game;")

        return self.cur.fetchone()[0]

    def makeFaction(self, faction_name, game_id):
        self.cur.execute("INSERT INTO diplomacy.faction (gameid, name) VALUEs (%s, %s);", (game_id, faction_name))
        self.conn.commit()
        self.cur.execute("SELECT max(id) FROM diplomacy.faction;")
        return self.cur.fetchone()[0]

    def makePlayer(self, first_name, last_name):
        self.cur.execute("INSERT INTO diplomacy.player (firstname, lastname) "
                         "VALUES (%s, %s);", (first_name, last_name))
        self.conn.commit()
        self.cur.execute("SELECT max(id) FROM diplomacy.player;")
        return self.cur.fetchone()[0]

    def makeColor(self, name, r, g, b):
        self.cur.execute("INSERT INTO diplomacy.color (name, r, g, b) VALUES "
                         "(%s, %s, %s, %s);", (name, r, g, b))
        self.conn.commit()

    def makeUnit(self, is_naval, location_id, faction_id):
        self.cur.execute("INSERT INTO diplomacy.unit (isnaval, location, "
                         "curorder, factionid) VALUES (%s, %s, NULL, %s);",
                         (is_naval, location_id, faction_id))
        self.conn.commit()
        self.cur.execute("SELECT max(id) FROM diplomacy.unit;")
        return self.cur.fetchone()[0]

    def makeUnitOrder(self, type_id, target_id):
        self.cur.execute("INSERT INTO diplomacy.unitorder (type, target) VALUES"
                         " (%s, %s);", (type_id, target_id))
        self.conn.commit()
        self.cur.execute("SELECT max(id) FROM diplomacy.unitorder;")
        return self.cur.fetchone()[0]

    def makeLocation(self, x_pos, y_pos, is_poi, type_id, owner_faction_id):
        self.cur.execute("INSERT INTO diplomacy.location (xpos, ypos, ispoi, "
                         "type, factionid) VALUES (%s, %s, %s, %s, %s);", (x_pos,
                         y_pos, is_poi, type_id, owner_faction_id))
        self.conn.commit()
        self.cur.execute("SELECT max(id) FROM diplomacy.location;")
        return self.cur.fetchone()[0]

    def makeNeighbors(self, ida, idb):
        if idb < ida:
            temp = ida
            ida = idb
            idb = temp

        self.cur.execute("INSERT INTO diplomacy.neighbor (locida, locidb) VALUES"
                         " (%s, %s);", (ida, idb))
        self.conn.commit();

    # def makeLocType(self, name):
    #     self.cur.execute("INSERT INTO diplomats.loctype (name) VALUES (%s);", (name))
    #     self.conn.commit()
    #     self.cur.execute("SELECT max(id) FROM diplomats.loctypes")
    #     return self.cur.fetchone()[0]

    """ =========== GETTERS =============== """

    def getAttacks(self, gameId):
        self.cur.execute("SELECT * FROM get_order_of_type(%s, 2);", gameId)
        return self.cur.fetchall()

    def getOrigin(self, orderId):
        self.cur.execute("SELECT * FROM get_origin(%s);", orderId)

    def getDefenses(self, gameId):
        self.cur.execute("SELECT * FROM get_order_of_type(%s, 3);", gameId)
        return self.cur.fetchall()

    def getOrder(self, unitId):
        self.cur.execute("SELECT unitorder.id FROM diplomacy.unitorder, "
                         "diplomacy.unit WHERE unit.orderId = %s AND "
                         "unitorder.id = %s;", (unitId, unitId))
        return self.cur.fetchone()

    def getUnit(self, locId):
        self.cur.execute("SELECT * FROM get_unit_at(%s);", locId)
        return self.cur.fetchone()

    def getOrdersAttacking(self, locId):
        self.cur.execute("SELECT * FROM get_orders_on(%s, 2);", locId)
        return self.cur.fetchall()

    def getConvoys(self, gameId):
        self.cur.execute("SELECT * FROM get_order_of_type(%s, 5);", gameId)
        return self.cur.fetchall()

    def isEmpty(self, locId):
        self.cur.execute("SELECT * FROM loc_is_empty(%s);", locId)
        return self.cur.fetchone()

    def getNeighbors(self, locId):
        self.cur.execute("SELECT * FROM diplomacy.neighbor WHERE locida=%s OR locidb=%s", (locId, locId));
        return self.cur.fetchall()

    """ ========== MISC ========= """

    def removeLocation(self, id):
        self.cur.execute("DELETE FROM diplomacy.location WHERE id=%s;" % id)
        self.conn.commit()

    def removePlayer(self, id):
        self.cur.execute("DELETE FROM diplomacy.player WHERE id=%s;" % id);
        self.conn.commit()

    def removeFaction(self, id):
        self.cur.execute("DELETE FROM diplomacy.faction WHERE id=%s;" % id);
        self.conn.commit()

    def removeGame(self, id):
        self.cur.execute("DELETE FROM diplomacy.game WHERE gameid=%s;" % id);
        self.conn.commit()

    def removeUnit(self, id):
        self.cur.execute("DELETE FROM diplomacy.unit WHERE id=%s;" % id);
        self.conn.commit()

    def removeNeighbors(self, ida):
        self.cur.execute("DELETE FROM diplomacy.neighbor WHERE locida=%s" % ida)