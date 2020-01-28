from django.test import TestCase
from sharing.models import Payments, Access, Rents
from django.utils import timezone
from datetime import datetime, timedelta
import json
import requests

data = {
    "id": 10
}

data = json.dumps(data)

response = requests.post("http://127.0.0.1:8000/bitx/",data=data)
print(response.text)


