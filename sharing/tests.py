from django.test import TestCase
from .models import *
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Q
import random
from django.utils import timezone

for i in range(200):
    r = random.randint(i,200)
    Rents.renta.createRent(1,1,
        timezone.now() + timedelta(days=r),
        timezone.now() + timedelta(days=r+r),
        
        )
