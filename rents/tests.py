from django.test import TestCase
from sharing.models import UsersDocuments, Rents, Access
from django.db.models import Q
# Create your tests here.
from datetime import datetime
from django.utils import timezone
start =  datetime(2019,12,11,21,59)
end =  datetime(2019,12,12,21,59)

renta = Rents.objects.filter(rentor_id=1,end__lt=timezone.now())
print(renta)