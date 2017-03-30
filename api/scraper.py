import web
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import urllib2
from datetime import datetime
from config import Config
from lxml import etree
from eventshandle import EventsHandle
import sys
import dateutil.parser
handle = EventsHandle(Config.dbname, Config.dbuser, Config.dbhost, Config.dbpass)

########### Rutgers seminars ###########

# urls = ['https://ruevents.rutgers.edu/events/getEventsRss.xml?categoryId=12',
#         'https://ruevents.rutgers.edu/events/getEventsRss.xml?categoryId=14',
#         'https://ruevents.rutgers.edu/events/getEventsRss.xml?categoryId=15',
#         'https://ruevents.rutgers.edu/events/getEventsRss.xml?categoryId=16']
#
# for url in urls:
#     tree = etree.parse(urllib2.urlopen(url))
#     root = tree.getroot()
#
#     for element in root.iter():
#         if element.tag == 'title':
#             handle.title = element.text
#         elif element.tag == 'description':
#             handle.description = element.text
#         elif element.tag == 'link':
#             handle.link = element.text
#         elif element.tag == '{http://ruevents.rutgers.edu/events}beginDateTime':
#             handle.date = int(datetime.strptime(element.text, '%Y-%m-%d %H:%M:%S %a').strftime('%s'))
#         elif element.tag == '{http://ruevents.rutgers.edu/events}location':
#             handle.location = element.text
#             if handle.location == 'Online':
#                 handle.online = True
#         elif element.tag == '{http://ruevents.rutgers.edu/events}address' and not handle.online:
#             handle.address = element.text
#         elif element.tag == '{http://ruevents.rutgers.edu/events}city' and not handle.online:
#             handle.address += ', ' + element.text
#         elif element.tag == '{http://ruevents.rutgers.edu/events}state' and not handle.online:
#             handle.address += ', ' + element.text
#         elif element.tag == '{http://ruevents.rutgers.edu/events}speaker':
#             handle.speaker = element.text
#         elif element.tag == '{http://ruevents.rutgers.edu/events}sponsor':
#             handle.sponsor = element.text
#         elif element.tag == '{http://ruevents.rutgers.edu/events}fee':
#             handle.fee = element.text
#             handle.department = 'Rutgers Events'
#             handle.insertRow('link', handle.link)
#
#     handle.commitRows()


url = 'http://www.physics.rutgers.edu/colloquium/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

table = soup.find('table')

for row in table.find_all('tr')[1:]:

    columns = row.find_all('td')

    column1 = columns[0]
    datestr = ''
    for i in column1.contents:
        if i != u'\n' and type(i) != Tag:
            datestr += i.strip() + ' '
    datestr += str(datetime.now().year) + ' 16:30'
    handle.ts = dateutil.parser.parse(datestr).strftime('%s')

    column2 = columns[1]

    if 'no colloquium' in column2.text.lower().strip():
        print 'no q'
        print column2
