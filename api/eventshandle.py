import sys
import psycopg2
import unicodedata
# from exceptions import UnicodeWarning
# from warnings import filterwarnings
# filterwarnings(action="error", category=UnicodeWarning)

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

    def sanitizeRow(self):
        self.toinsert = [self.title, self.link, self.description, self.date, self.location, self.address, self.speaker, self.sponsor, self.fee, self.department, 0]

        self.toinsert = [el.encode('utf-8') if type(el) == unicode else el for el in self.toinsert]

    def insertRow(self, column, identifier):

        self.sanitizeRow()

        self.reset()

        #query = 'INSERT INTO events (title, link, description, ts, location, address, speaker, sponsor, fee, category) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        # self.cur.execute(query % (self.title, self.link, self.description, self.date, self.location, self.address, self.speaker, self.sponsor, self.fee, self.category))

        self.cur.execute("SELECT * FROM events WHERE %s = '%s'" % (column, identifier))
        rows = self.cur.fetchall()

        outdated = False

        if len(rows) > 0:

            for row in rows:
                for col in row:
                    if row.index(col) != 0:

                        if col == None or type(col) == int:
                            if col != self.toinsert[row.index(col) - 1]:
                                outdated = True
                        else:
                            if col != self.toinsert[row.index(col) - 1]:
                                outdated = True

                if outdated:
                    self.cur.execute("UPDATE events SET version = version + 1 WHERE %s = '%s'" % (column, identifier))
                    print "updating old verion"

            if outdated:
                query = 'INSERT INTO events (title, link, description, ts, location, address, speaker, sponsor, fee, department, version) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                self.cur.execute(query, self.toinsert)
                print "inserting updated row"

        else:
            query = 'INSERT INTO events (title, link, description, ts, location, address, speaker, sponsor, fee, department, version) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            self.cur.execute(query, self.toinsert)
            print "inserting for the first itme"

            self.cur.execute("SELECT * FROM departments WHERE department = '%s'" % self.toinsert[9])

            if len(self.cur.fetchall()) == 0:
                self.cur.execute("INSERT INTO departments (department) VALUES ('%s')" % self.toinsert[9])

            # change department table and column to be relational

    def commitRows(self):

        self.con.commit()
        self.reset()

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
