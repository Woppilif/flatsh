from django.test import TestCase

from sharing.models import Access, Rents, Flats, Images
from django.contrib.auth.models import User
from rents.modules import bitx
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import datetime
import requests


soap = bitx.Soap()
for i in soap.getAll():
    soap.parse_data(i)

        


