import sys
import psycopg2

class EventsHandle():

    def __init__(self, dbname, dbuser, dbhost, dbpass):
        self.toinsert = []
        self.title = None
        self.link = None
        self.description = None
        self.date = 0
        self.location = None
        self.address = None
        self.speaker = None
        self.sponsor = None
        self.online = False
        self.fee = None
        self.category = None

        try:
            self.con = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (dbname, dbuser, dbhost, dbpass))
        except:
            print 'Unable to connect to db.'
            sys.exit()

        self.cur = self.con.cursor()

    def addRow(self):
        self.toinsert.append((self.title, self.link, self.description, self.date, self.location, self.address, self.speaker, self.sponsor, self.fee, self.category))
        self.title = None
        self.link = None
        self.description = None
        self.date = 0
        self.location = None
        self.address = None
        self.speaker = None
        self.sponsor = None
        self.online = False
        self.fee = None
        self.category = None

    def insertEvents(self):

        #query = 'INSERT INTO events (title, link, description, ts, location, address, speaker, sponsor, fee, category) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        #args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%)", x) for x in tup)

        #self.con.commit()
        #self.toinsert = []
        pass

    def insertRow(self):

        query = '''INSERT INTO events (title, link, description, ts, location, address, speaker, sponsor, fee, category)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''' %
                (self.title, self.link, self.description, self.date, self.location, self.address, self.speaker, self.sponsor, self.fee, self.category)

    def reset(self):
        self.toinsert = []
        self.title = None
        self.link = None
        self.description = None
        self.date = 0
        self.location = None
        self.address = None
        self.speaker = None
        self.sponsor = None
        self.online = False
        self.fee = None
        self.category = None
