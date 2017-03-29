import web
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import urllib2
from datetime import datetime
from config import Config
from lxml import etree
from eventshandle import EventsHandle
import sys
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
