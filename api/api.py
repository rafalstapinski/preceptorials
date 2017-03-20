import web
import requests
from lxml import html



page = requests.get('http://benedick.rutgers.edu/fermentation/')
tree = html.fromstring(page.content)

content = tree.xpath('//div[@id="content"]/text()')

print content
