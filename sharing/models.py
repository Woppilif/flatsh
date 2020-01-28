from django.db import models
from django.contrib.auth.models import User
import uuid
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from PIL import Image
from yandex_checkout import Payment,Configuration 
from django.conf import settings
from phone_field import PhoneField
import decimal
Configuration.account_id = settings.YA_ACCOUNT_ID
Configuration.secret_key = settings.YA_SECRET_KEY

#from .managers import PersonManager

# Create your models here.
class Countries(models.Model):
    country_name = models.CharField(max_length=200)
    def __str__(self):
        return self.country_name
    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

class Cities(models.Model):
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=200)
    def __str__(self):
        return self.city_name
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

class Partners(models.Model):
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    headmaster = models.CharField(default=None,blank=True,null=True,max_length=60)
    hmrank = models.CharField(default=None,blank=True,null=True,max_length=60)
    org_name = models.CharField(default=None,blank=True,null=True,max_length=60)
    document = models.CharField(default=None,blank=True,null=True,max_length=60)

    def __str__(self):
        return str(self.account)

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'
    
    def CheckUserPartner(self):
        return self.account

class Workers(models.Model):
    SHIRT_SIZES = (
        (1, 'Менеджер'),
        (2, 'Клининг'),
        (3, 'Мастер'),
    )
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE)
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(choices=SHIRT_SIZES)
    chat_id = models.IntegerField(default=None,blank=True,null=True)
    def __str__(self):
        return str(self.account)

    class Meta:
        verbose_name = 'Сотрудник партнёра'
        verbose_name_plural = 'Сотрудники партнёров'   

    def CheckUserWorker(self):
        return self.account
        '''
        try:
            return Workers.objects.get(account=self.account)
        except:
            return False
        return True 
        '''

class Districts(models.Model):
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=200)
    def __str__(self):
        return self.district_name

    def city(self):
        return self.partner.city

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'

class FlatManager(models.Manager):

    def get_flat(self,flat_id):
        try:
            self.get(device__pk=flat_id)
            return True
        except:
            return False
        

    def update_flat_status(self,flat_id,status):
        if self.get_flat(flat_id):
            flat =  self.get(device__pk=flat_id)
            flat.device.status = status
            flat.device.save()
            return True
        return False

def device_status(value):
    print()
    print("This is device_status")
    print(value)

class Devices(models.Model):
    open_key = models.CharField(max_length=60, blank=True, null=True)
    secret_key = models.CharField(max_length=60, blank=True, null=True,default=None)
    app_status = models.BooleanField(blank=True, null=True,default=None)
    created_at = models.DateTimeField(null=True,blank=True,default=None)
    status = models.BooleanField(null=True,default=False,validators=[device_status])
    description = models.CharField(max_length=60, blank=True, null=True,default=None)

    def flatId(self):
        return Flats.objects.filter(device=self).first()    
    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'

class Flats(models.Model):
    DOOR_STATS = (
        (False, 'Заблокирована'),
        (True, 'Доступ открыт')
    )
    FLAT_STATS = (
        ('BLOCKED', 'Заблокирована'),
        ('RENTED', 'Арендована'),
        ('BUCHEN', 'Забронирована'),
        ('U', 'Свободна')
    )
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)#
    street = models.CharField(max_length=50, blank=True, null=True)#
    house_number = models.CharField(max_length=10, blank=True, null=True)
    building = models.CharField(max_length=10, blank=True, null=True)
    flat_number = models.CharField(max_length=10, blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    rooms = models.IntegerField(blank=True, null=True,default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    per_hour = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    hint = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=10,blank=True, null=True,choices=FLAT_STATS)
    door_status = models.BooleanField(blank=True, null=True,choices=DOOR_STATS)
    cleaning_time = models.TimeField(blank=True, null=True,default="3:00")
    bxcal_id = models.IntegerField(blank=True, null=True,default=None)
    metro_station = models.CharField(max_length=60, blank=True, null=True)
    internal_id = models.CharField(max_length=60, blank=True, null=True)



    device = models.ForeignKey(Devices, on_delete=models.CASCADE,default=None, blank=True, null=True)

    flas = FlatManager()
    objects = models.Manager()

    def __str__(self):
        return "{0} {1}".format(self.street,self.district.district_name)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('rents:apartment', args=[int(self.pk)])

    def flatsItems(self):
        return FlatsItems.objects.filter(flat_id=self.pk)

    def partnerInfo(self):
        return self.district.partner

    def addressPartOne(self):
        return "{0}, {1}, {2} {3}".format(self.city(),self.district,self.street,self.HouseNumber())

    def addressPartTwo(self):
        return "кв. {0} этаж {1}".format(self.flat_number,self.floor)

    def HouseNumber(self):
        if self.building is None:
            return self.house_number
        return "{0} к.{1}".format(self.house_number,self.building)

    def city(self):
        return self.district.city()

    def address(self):
        return "{0} {1}".format(self.street,self.HouseNumber())

    city.admin_order_field = 'city'
    city.short_description = 'Город'

    def partner(self):
        return str(self.district.partner)

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'

    def getCurrentRent(self):
        return Rents.objects.filter(start__lte=timezone.now(),end__gt=timezone.now(),flat=self).last()

    def getRents(self):
        return Rents.objects.filter(Q(start__gte=timezone.now()) | Q(start__lte=timezone.now()),flat=self,end__gte=timezone.now())

    def getStatus(self):
        rent = Rents.objects.filter(start__lte=timezone.now(),end__gt=timezone.now(),flat_id=self.id,status=True).last()
        if rent is not None:
            return "Занята"
        return "Свободна"

    def getImages(self):
        return Images.objects.filter(flat_id=self.pk)
    
    def getPreview(self):
        return Images.objects.filter(flat_id=self.pk).first()

    def getCurrentRenta(self,date):
        return Rents.objects.filter(flat=self,start__lte=date,end__gte=date,status=True,paid=True).last()

    def getFirstFutureRenta(self,date):
        return Rents.objects.filter(flat=self,start__gte=date,status=True,paid=True).last()

class FlatsItems(models.Model):
    flat = models.ForeignKey(Flats, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50, blank=True, null=True,verbose_name="Предмет (Стол, стул)")
    item_count = models.IntegerField(blank=True,null=True,default=0,verbose_name="Количество предметов (целое число)")
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return "{0} {1} шт.".format(self.item_name,self.item_count)

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('flats/images', filename)

def get_file_path_users(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('users/images', filename)

class Images(models.Model):
    flat = models.ForeignKey(Flats, on_delete=models.CASCADE)
    images = models.CharField(max_length=255,blank=True, null=True,default=None)
    #models.ImageField(blank=True, null=True,upload_to=get_file_path,default='/imgs/home.png')
    img_url = models.CharField(max_length=255,blank=True, null=True,default=None)
    urled = models.BooleanField(blank=True, null=True,default=False)

    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
    '''
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, str(self.images)))
        super(Images,self).delete(*args,**kwargs)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.images.path)
        width, height = img.size  # Get dimensions

        if width > 500 and height > 300:
            # keep ratio but shrink down
            img.thumbnail((width, height))

        # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 500 and height > 300:
            img.thumbnail((500, 300))

        img.save(self.images.path)
    '''

class RentsManager(models.Manager):

    def createRent(self,flat,user,start,end):
        return self.create(flat=flat,rentor=user,start=start,end=end,status=True,created_at=timezone.now(),booking=start + timedelta(hours=2))
    
    def createRentExt(self,flat,user,start,end):
        return self.update_or_create(flat=flat,rentor=user,start=start,end=end,status=True,paid=True,booking=start + timedelta(hours=2))

class Rents(models.Model):
    flat = models.ForeignKey(Flats, on_delete=models.CASCADE,related_name="Квартира",related_query_name="Квартира")
    rentor = models.ForeignKey(User, models.DO_NOTHING)
    start = models.DateTimeField(verbose_name='Начало аренды',null=True,default=None)
    end = models.DateTimeField(verbose_name='Окончание аренды',null=True,default=None)
    booking = models.DateTimeField(null=True,blank=True,verbose_name='Окончание бронироваия',default=None)
    status = models.BooleanField(null=True,default=False)
    paid = models.BooleanField(null=True,default=False)
    created_at = models.DateTimeField(null=True,blank=True,default=None)
    trial_key = models.CharField(max_length=80, blank=True, null=True,default=None)
    renta = RentsManager()
    objects = models.Manager()
    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'
        ordering = ['-start']

    def get_absolute_url(self):
        from django.urls import reverse
        if self.trial_key is not None:
            return reverse('rents:trial_renta', args=[self.trial_key])

    def __str__(self):
        return "{0} с {1} по {2}".format(self.flat,self.start,self.end)
    
    def status_info(self):
        if self.status is True:
            return 'Подтверждена'
        return 'Не подтверждена'

    def Location(self):
        return self.flat

    def startDate(self):
        return str(self.start)

    def endDate(self):
        return str(self.end)
  
    def AccessObj(self):
        return Access.objects.filter(renta=self.id,user=self.rentor).last()

    def getDays(self):
        days = (self.end-self.start).days
        if days < 1:
            return 1
        return days

    def getPrice(self):
        return self.getDays() * self.flat.price

    def getDeposit(self):
        return self.flat.deposit

    def getPayments(self):
        return Payments.objects.filter(renta=self)


class Payments(models.Model):
    P_TYPES = (
        (0, 'Подтверждение аккаунта'),
        (1, 'Депозит'),
        (2, 'Полная стоимость'),
        (3, 'Оплата картой клиента')
    )
    PAID_TYPES = (
        (False, 'Не оплачен'),
        (True, 'Оплачен'),
        (None, 'Отменён / Возвращён')
    )
    rentor = models.ForeignKey(User, models.DO_NOTHING,blank=True, null=True)
    renta = models.ForeignKey(Rents, on_delete=models.CASCADE,blank=True, null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateTimeField(null=True,blank=True)
    status = models.BooleanField(null=True,default=False,choices=PAID_TYPES)
    payment_type = models.IntegerField(blank=True, null=True,choices=P_TYPES,default=0)
    payment_id = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(null=True,blank=True)
    expires_at = models.DateTimeField(null=True,blank=True)
    captured_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return "{0} {1}. Дата и время создания: {2}".format(self.price,self.transactionStatus(),self.date)

    def transactionStatus(self):
        return [i for i in self.PAID_TYPES if i[0] == self.status][0][1]

    def get(self):
        return Payment.find_one(self.payment_id)

    def cancel(self):
        self.status = None
        self.save()
        return Payment.cancel(self.payment_id,str(uuid.uuid4()))

    def capture(self):
        return Payment.capture(
            self.payment_id,
            {
                "amount": {
                    "value": self.price,
                    "currency": "RUB"
                }
            },
            str(uuid.uuid4()) #idempotence key
        )
    
    def payPrice(self):
        if self.rentor is None:
            print("r")
            return None
        if self.price is None:
            print("p")
            return None
        if self.payment_type != 2:
            print("pt")
            return None
        if self.status is True:
            print("s")
            return None
        return Payment.create({
            "amount": {
                "value": self.renta.getPrice(),
                "currency": "RUB"
            },
            "capture": "true",
            "payment_method_id": self.rentor.usersdocuments.yakey,
            "description": "Заказ ID:{0}".format(self.pk)
        })

    def rentaPaid(self):
        if self.status is False:
            return None
        self.renta.paid = True
        self.renta.save()
        return self

    def setStatus(self):
        if self.payment_status == 'canceled':
            self.status = None
        elif self.payment_status == 'succeeded':
            self.status = True
        self.save()
        return self

    def setInfo(self,paymentObject):
        if paymentObject is None:
            return None
        self.payment_id = paymentObject.id
        self.payment_status = paymentObject.status
        self.created_at = paymentObject.created_at
        self.expires_at = paymentObject.expires_at
        self.save()
        return self


    def findOne(self):
        if self.payment_id is None:
            return None
        return Payment.find_one(self.payment_id)

    def createPaymentObject(self,capture = False, save_payment_method = True):
        '''
            Returns Yandex Kassa Object if rentor i.e user and price are set.
        '''
        if self.rentor is None:
            return None
        if self.price is None:
            return None
        return Payment.create({
            "amount": {
                "value": "{0}".format(str(decimal.Decimal(self.price))),
                "currency": "RUB"
            },

            "confirmation": {
                "type": "embedded"
            },
            "receipt": {
            "customer": {
                "full_name": "{0} {1}".format(self.rentor.first_name,self.rentor.last_name),
                "email": "{0}".format(self.rentor.email)
            },
            "items": [
                    {
                        "description": "Оплата аренды",
                        "quantity": "2.00",
                        "amount": {
                            "value": "{0}".format(str(decimal.Decimal(self.price))),
                            "currency": "RUB"
                        },
                        "vat_code": "2",
                        "payment_mode": "full_prepayment",
                        "payment_subject": "commodity"
                    }
                ]
            },
            "capture": capture,
            "save_payment_method": save_payment_method,
            "description": "Оплата аренды №{0}".format(self.pk)
        })

    class Meta:
        verbose_name = 'Транзакция Yandex'
        verbose_name_plural = 'Транзакции Yandex'


class SystemLogs(models.Model):
    device = models.ForeignKey(Devices, models.DO_NOTHING,blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING,blank=True, null=True)
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE,blank=True, null=True)
    worker = models.ForeignKey(Workers, on_delete=models.CASCADE,blank=True, null=True)
    district = models.ForeignKey(Districts, on_delete=models.CASCADE,blank=True, null=True)
    flat = models.ForeignKey(Flats, on_delete=models.CASCADE,blank=True, null=True)
    payment = models.ForeignKey(Payments, on_delete=models.CASCADE,blank=True, null=True)
    rents = models.ForeignKey(Rents, on_delete=models.CASCADE,blank=True, null=True)
    created_at = models.DateTimeField(null=True,blank=True)
    comment = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "{0} - {1}".format(self.comment,self.created_at)

class AccessManager(models.Manager):
    def createAccess(self,renta):
        return self.create(user=renta.rentor,renta=renta,stype=False)

    def createPaidAccess(self,renta):
        if renta.paid is True:
            return self.get_or_create(user=renta.rentor,renta=renta,stype=True,start=renta.start,end=renta.end)
        return False

    def setFreeTime(self):
        if self.end is None:
            now = timezone.now()
            if (now >= self.renta.start):
                self.start = now
                self.end = self.start + timedelta(minutes=10)
                self.save()
                return self
        return None

    def setPaidTime(self):
        if self.renta.paid is True:
            self.start = self.renta.start,
            self.end = self.renta.end,
            self.stype = True
            self.save()
            return self
        return None

class Access(models.Model):
    PAID_TYPES = (
        (False, 'Осмотр'),
        (True, 'Аренда')
    )
    user = models.ForeignKey(User, models.DO_NOTHING,blank=True, null=True)
    renta = models.ForeignKey(Rents, on_delete=models.CASCADE,blank=True, null=True)
    start = models.DateTimeField('Start',blank=True, null=True)
    end = models.DateTimeField('End',blank=True, null=True)
    used = models.IntegerField(blank=True, null=True,default=0)
    stype = models.BooleanField(null=False,default=False,choices=PAID_TYPES)

    access = AccessManager()
    objects = models.Manager()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('sharing:access', args=[int(self.pk)])



    def setFreeTime(self):
        if self.end is None:
            now = timezone.now()
            if (now >= self.renta.start):
                self.start = now
                self.end = self.start + timedelta(minutes=10)
                self.save()
                return self
        return None

    def setPaidTime(self):
        if self.renta.paid is True:
            self.start = self.renta.start,
            self.end = self.renta.end,
            self.stype = True
            self.save()
            return self
        return None

    def CheckAccess(self):
        if self.end is not None:
            now = timezone.now()
            print("{0} {1} {2}".format(now,self.start,self.end))
            if (now > self.start) and (now < self.end):
                return True
        return False

    def setStartTime(self):
        if self.end is None:
            now = timezone.now()
            print(now)
            if (now >= self.renta.start):
                self.start = timezone.now()
                self.end = self.start + timedelta(minutes=10)
                self.stype = False
                self.save()
        return False

    def timeRemaining(self):
        import time
        if self.end is not None:
            now = timezone.now()
            if (now > self.start) and (now < self.end):
                return "у вас осталось {0} минут".format(str(self.end - now))
            else:
                if (now < self.start):
                    return "Доступна с {0}".format(timezone.make_naive(self.start).strftime("%b %d %Y %H:%M:%S"))
                return "Время осмотра закончилось"
        else:
            return "осталось 10 минут"

    def usedAdd(self):
        self.used+=1
        self.save()


class UsersDocuments(models.Model):
    PAID_TYPES = (
        (False, 'Не подтвержден'),
        (True, 'Подтверждён')
    )
    PAID_TYPES = (
        (False, 'Не подтверждён'),
        (True, 'Подтверждён')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50,default="", blank=False, null=False,verbose_name="Имя")
    lastname = models.CharField(max_length=50,default="", blank=False, null=False,verbose_name="Фамилия")
    phone_number = PhoneField(blank=True, help_text='Contact phone number')
    #phone_number = models.CharField(max_length=50,default="", blank=False, null=False,verbose_name="Мобильный номер")
    image_one = models.ImageField(upload_to=get_file_path_users,default=None,verbose_name="Фотография первой страницы паспорта")
    image_two = models.ImageField(upload_to=get_file_path_users,default=None,verbose_name="Фотография страницы с пропиской")
    status = models.BooleanField(null=False,default=False,choices=PAID_TYPES)
    yakey = models.CharField(max_length=50,default=None, blank=False, null=True)
    ya_card_type = models.CharField(max_length=50,default=None, blank=False, null=True)
    ya_card_last4 = models.CharField(max_length=4,default=None, blank=False, null=True)
    totlal_cancelation = models.IntegerField(null=True,default=0,blank=True)    

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Документы пользователей'
        verbose_name_plural = 'Документы пользователей'

    def addCard(self,payment):
        self.yakey = payment.payment_method.id
        self.ya_card_type = payment.payment_method.card.card_type
        self.ya_card_last4 = payment.payment_method.card.last4
        self.save()

    def deleteCard(self):
        self.yakey = None
        self.ya_card_type = None
        self.ya_card_last4 = None
        self.save()
    
class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flat = models.ForeignKey(Flats, on_delete=models.CASCADE,blank=True, null=True)
    class Meta:
        verbose_name = 'Закладка пользователя'
        verbose_name_plural = 'Закладки пользователей'






    













