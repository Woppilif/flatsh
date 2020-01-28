from django.test import TestCase
from ics import Calendar
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from sharing.models import Payments, Access, Rents
'''
soup = BeautifulSoup(page.content, "lxml-xml")
print(soup.find("generation-date").get_text(strip=True))

for flat in soup.find_all("offer"):
    print(flat.get("internal-id"))
    print(flat.find("type").get_text(strip=True))


flat_id = 10

url = "https://www.laps.r73.ru/dum/iCal/bxcal{0}.ics".format(flat_id)
c = Calendar(requests.get(url).text)
for i in c.events:
    print(i.name)
    print(i.begin)
    print(i.end)


url = "https://www.laps.r73.ru/dum/ya/ya.xml"
root = ET.fromstring(requests.get(url).text)
for item in root.findall("."):
    for child in item:
        print(child)
'''
