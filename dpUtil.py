import psycopg2

class DB():
    def __init__(self, schema_filename):
        self.conn = psycopg2.connect("dbname=diplomats user=postgres")
        self.cur = conn.cursor()
        self.cur.execute(open(schema_filename, "r").read())
        conn.commit()
        print("Initialized DB")

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def getAttacks(gameId):
        self.cur.execute("SELECT * FROM get_order_of_type(%s, 2);", gameId)
        return self.cur.fetchall()

    def getOrigin(orderId):
        self.cur.execute("SELECT * FROM get_origin(%s);")

    def getDefenses(gameId):
        self.cur.execute("SELECT * FROM get_order_of_type(%s, 3);", gameId)
        return self.cur.fetchall()

    def getOrder(unitId):
        self.cur.execute("SELECT unitorder.id FROM diplomacy.unitorder, diplomacy.unit WHERE unit.orderId = %s AND unitorder.id = %s;", unitId, unitId)
        return self.cur.fetchone()

    def getUnit(locId):
        self.cur.execute("SELECT * FROM get_unit_at(%s);", locId)
        return self.cur.fetchone()

    def getOrdersAttacking(locId):
        self.cur.execute("SELECT * FROM get_orders_on(%s, 2);", locId)
        return self.cur.fetchall()

    def getConvoys(gameId):
        self.cur.execute("SELECT * FROM get_order_of_type(%s, 5);", gameId)
        return self.cur.fetchall()

    def isEmpty(locId):
        self.cur.execute("SELECT * FROM loc_is_empty(%s);", locId)
        return self.cur.fetchone()
