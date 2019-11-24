from django.test import TestCase
from sharing.models import *
# Create your tests here.


renta =  Rents.objects.get(pk=25)
print(renta.paid)
access = Access.access.createAccess(renta)

print(access.setPaidTime())