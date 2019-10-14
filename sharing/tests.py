from django.test import TestCase
from .models import *
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Q
import random
from django.utils import timezone

rr = Rents.objects.all()
print(rr)
for x in rr:
    start = x.end + timedelta(days=0)
    end = x.end + timedelta(days=10)
    rented = Rents.objects.filter(Q(start__gte=start) | Q(start__lte=start, end__gte=end),flat=x.flat,status=True)
    print(rented.count())