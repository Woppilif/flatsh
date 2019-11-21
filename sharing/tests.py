from django.test import TestCase
from .models import *
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Q
from sharing.models import Rents
import random
from django.utils import timezone

Rents.objects.create(flat_id=1, rentor_id=1,start=datetime.now()-timedelta(days=3),end=datetime.now()-timedelta(days=2))

print(Rents.objects.all())

rents = Rents.objects.filter(start__gte=timezone.now(),end__lte=timezone.now())

print(rents)