import web
import json

def write(payload, status):
    return json.dumps({'payload': payload, 'status': status})

def notfound():
    return web.notfound('404')

def new_request(request):
    web.header('Content-Type', 'application/json')
    web.header('Access-Control-Allow-Origin', '*')

urls = (
    '/events/get', 'events_get',

)

class events_get():
    def GET(self):

        webinput = web.input()

        try:
            f = webinput['filter'].encode('utf-8')
        except UnicodeError:
            return write({'message': 'Filter not UTF-8 encoded. '}, 400)
        except UnicodeError:
            return write({'message': 'Filter not supplied. '}, 400)

        

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.notfound = notfound
    app.run()
