from django.test import TestCase
from .models import *
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Q
from sharing.models import Rents
import random
from django.utils import timezone

rents = Rents.objects.filter(start__gte=timezone.now(),booking__lte=timezone.now(),status=True,paid=False)

print(rents)