from django.db import models

# Create your models here.

class UserAccount(models.Model):
    email = models.EmailField(max_length=80, blank=False, null=False,default=None,verbose_name="Электронная почта для отправки чека об оплате")
    first_name = models.CharField(max_length=80, blank=False, null=False,default=None,verbose_name="Имя")
    last_name = models.CharField(max_length=80, blank=False, null=False,default=None,verbose_name="Фамилия")
    price  =  models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Сумма",blank=False, null=False,default=None)
    key = models.CharField(max_length=80, blank=True, null=True,default=None)
    status = models.BooleanField(null=True,default=False)
    created_at = models.DateTimeField(null=True,default=None)
    payment_id = models.CharField(max_length=50, blank=True, null=True,default=None)


