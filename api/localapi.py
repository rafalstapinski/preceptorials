#! /usr/bin/env python

import web
import json
from config import Config
import urllib

from web.wsgiserver import CherryPyWSGIServer

# CherryPyWSGIServer.ssl_certificate = "/etc/letsencrypt/live/stapinski.co/fullchain.pem"
# CherryPyWSGIServer.ssl_private_key = "/etc/letsencrypt/live/stapinski.co/privkey.pem"

def write(payload, status):
    return json.dumps({'payload': payload, 'status': status})

def notfound():
    return web.notfound('404')

def new_request(request):
    web.header('Content-Type', 'application/json')
    web.header('Access-Control-Allow-Origin', '*')

urls = (
    '/preceptorials/api/events/get', 'events_get',
)

class events_get():
    def POST(self):

        new_request(self)

        webinput = web.input()

        try:

            print webinput['filters']

            filters = json.loads(webinput['filters'].encode('utf-8'))

            startdate = filters['date']['start']
            enddate = filters['date']['end']

        except UnicodeError:
            print 'not utf encoded'
            return write({'message': 'Filter not UTF-8 encoded. '}, 400)
        except KeyError:
            print 'no filter'
            return write({'message': 'Filter not supplied. '}, 400)
        except ValueError:
            print 'not in json format'
            return write({'message': 'Filter not in proper JSON format. '}, 400)


        db = web.database(dbn='postgres', db=Config.dbname, user=Config.dbuser, pw=Config.dbpass)
        events = db.select('events', dict(startdate=startdate, enddate=enddate), where='ts > $startdate AND ts < $enddate')

        result = []

        for event in events:
            result.append({'title': event.title, 'link': event.link,
                            'description': event.description, 'ts': event.ts,
                            'location': event.location, 'address': event.address,
                            'speaker': event.speaker, 'sponsor': event.sponsor,
                            'fee': event.fee, 'department': event.department})

        return write({'message': 'List of events matching criteria. ', 'events': result}, 200)


        # departments to relation

        # query = 'SELECT * FROM events WHERE department = %s'
        #
        # db = web.database(dbn='postgres', db=Config.dbname, user=Config.dbuser, pw=Config.dbpass)
        #
        # events = db.select('events', dict(department='ruevents'), where='department = $dept' )
        #
        # print events

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.notfound = notfound
    app.run()
