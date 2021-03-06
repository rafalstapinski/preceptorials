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
import re

class Scraper:

    def __init__(self, dept):

        self.run(dept)

    def run(self, dept):

        if dept == 'all':
            for attr in dir(self):
                if attr not in ['__init__', '__doc__', '__module__', 'run']:
                    getattr(self, attr)()

        else:
            getattr(self, dept)()

    def ruevents(self):

        urls = ['https://ruevents.rutgers.edu/events/getEventsRss.xml?categoryId=12',
                'https://ruevents.rutgers.edu/events/getEventsRss.xml?categoryId=14',
                'https://ruevents.rutgers.edu/events/getEventsRss.xml?categoryId=15',
                'https://ruevents.rutgers.edu/events/getEventsRss.xml?categoryId=16']

        for url in urls:
            tree = etree.parse(urllib2.urlopen(url))
            root = tree.getroot()

            for element in root.iter():
                if element.tag == 'title':
                    handle.title = element.text
                elif element.tag == 'description':
                    handle.description = element.text
                elif element.tag == 'link':
                    handle.link = element.text
                elif element.tag == '{http://ruevents.rutgers.edu/events}beginDateTime':
                    handle.date = int(datetime.strptime(element.text, '%Y-%m-%d %H:%M:%S %a').strftime('%s'))
                elif element.tag == '{http://ruevents.rutgers.edu/events}location':
                    handle.location = element.text
                    if handle.location == 'Online':
                        handle.online = True
                elif element.tag == '{http://ruevents.rutgers.edu/events}address' and not handle.online:
                    handle.address = element.text
                elif element.tag == '{http://ruevents.rutgers.edu/events}city' and not handle.online:
                    handle.address += ', ' + element.text
                elif element.stag == '{http://ruevents.rutgers.edu/events}state' and not handle.online:
                    handle.address += ', ' + element.text
                elif element.tag == '{http://ruevents.rutgers.edu/events}speaker':
                    handle.speaker = element.text
                elif element.tag == '{http://ruevents.rutgers.edu/events}sponsor':
                    handle.sponsor = element.text
                elif element.tag == '{http://ruevents.rutgers.edu/events}fee':
                    handle.fee = element.text
                    handle.department = 'Rutgers Events'
                    handle.insertRow('link', handle.link)

            handle.commitRows()

    def physics_colloquium(self):

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

            titlestr = ''

            a = column2.find('a')

            if a is not None:
                handle.link = 'http://www.physica.rutgers.edu/colloquium/' + a.attrs['href']
                print handle.link

            # for c in column2.contents:
            #     if type(c) is not Tag:
            #         t = ' '.join(c.split())
            #         if 'no colloquium' in t.lower():
            #             handle.ignore = True
            #             break
            #         elif t != ' ':
            #             titlestr += t

            # if not handle.ignore:
            #     print titlestr, '---'

            handle.reset()

            # print column2.contents
            #
            # print titlestr


scraper = Scraper('physics_colloquium')
