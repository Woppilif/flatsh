from bs4 import BeautifulSoup
from ics import Calendar
import requests
from sharing.models import Access, Rents, Flats, Images, SystemLogs
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

class Bitx():
    def __init__(self):
        self.internal_id = None
        self.calendar_id = None
        self.calendar_ev = None
        self.images      = []
        self.location    = {
            'country': "",
            'city': "",
            'address':"",
            'metro':"",
            'latitude':"",
            'longitude':""
        }
        self.price       = None
        self.floor       = None
        self.rooms       = None
        self.description = None

    def getCalendarUrl(self):
        return "https://www.laps.r73.ru/dum/iCal/bxcal{0}.ics".format(self.calendar_id)

    def create(self,data):
        self.internal_id = data.get("internal-id")
        self.calendar_id = data.find("bxcal").get_text(strip=True).split("bxcal")[1].split(".ics")[0]
        self.calendar_ev = Calendar(requests.get(self.getCalendarUrl()).text).events
        self.price = data.find("price").contents[0].get_text(strip=True)
        self.floor = data.find("floor").get_text(strip=True)
        self.rooms = data.find("rooms").get_text(strip=True)
        self.location['country'] = data.find("country").get_text(strip=True)
        self.location['city'] = data.find("locality-name").get_text(strip=True)
        self.location['address'] = data.find("address").get_text(strip=True)
        self.location['metro'] = data.find("metro").contents[0].get_text(strip=True)
        coords = data.find("latitude-longitude")
        if coords is not None:
            coords = coords.get_text(strip=True).split(',')
            print(coords)
            #self.location['latitude'] = coords[0]
            #self.location['longitude'] = coords[1]
        self.description = data.find("description").get_text(strip=True).replace("ЗАСЕЛЕНИЕ КРУГЛОСУТОЧНО!!!","")
        for i in data.find_all("image"):
            self.images.append(i.get_text(strip=True))
        return self

class Soap(object):
    def __init__(self):
        self.flats = []
        page = requests.get("https://www.laps.r73.ru/dum/flat/flat.xml")
        self.__soup = BeautifulSoup(page.content, "lxml-xml")
        
    def getByInternalId(self,internal_id):
        flat = self.__soup.find(attrs={"internal-id" : internal_id})
        self.flats.append(Bitx().create(flat))
        return self.flats

    def getAll(self):
        for flat in self.__soup.find_all("offer"):
            self.flats.append(Bitx().create(flat))
        return self.flats

    def parse_data(self,i):
        flat,created = Flats.objects.update_or_create(
            district_id = 1,
            internal_id = i.internal_id,
            bxcal_id = i.calendar_id,
        )
        flat.street = i.location['address']
        flat.metro_station = i.location['metro']
        flat.price = i.price
        flat.floor = i.floor
        flat.rooms = i.rooms
        #flat.latitude = i.location['latitude']
        #flat.longitude = i.location['longitude']
        flat.description = i.description
        flat.save()
        print(flat)
        
        for x in i.images:
            img, created = Images.objects.update_or_create(
                flat = flat,
                images = None,
                urled = True,
                img_url = x
            )
        
        for x in i.calendar_ev:
            start = x._begin.replace(hour=14,minute=0)
            end = x._end_time.replace(hour=11,minute=0)

            start = datetime.strptime(str(start)[:16], '%Y-%m-%dT%H:%M')
            end = datetime.strptime(str(end)[:16], '%Y-%m-%dT%H:%M')
        
            start = timezone.make_aware(start)
            end = timezone.make_aware(end)
            
            renta,created = Rents.renta.createRentExt(flat=flat,
                user=User.objects.get(pk=2),
                start=start,
                end=end
            )
            #renta.user=User.objects.get(pk=2)
            renta.save()
            if created is True:
                Access.access.createPaidAccess(renta)
        SystemLogs.objects.create(
            flat=flat,
            comment = "Информация обновлена {0}".format(flat)
        )
        return True
            