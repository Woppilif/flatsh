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

    def __str__(self):
        return str(self.account)

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'
    
    def CheckUserPartner(self):
        return self.account

class Workers(models.Model):
    SHIRT_SIZES = (
        (1, 'Оператор'),
        (2, 'Клининг'),
        (3, 'Мастер'),
    )
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE)
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(choices=SHIRT_SIZES)
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
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    street = models.CharField(max_length=50, blank=True, null=True)
    house_number = models.CharField(max_length=10, blank=True, null=True)
    building = models.CharField(max_length=10, blank=True, null=True)
    flat_number = models.CharField(max_length=10, blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    per_hour = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10,blank=True, null=True,choices=FLAT_STATS)
    door_status = models.BooleanField(blank=True, null=True,choices=DOOR_STATS)
    cleaning_time = models.TimeField(blank=True, null=True,default="3:00")
    app_id = models.CharField(max_length=60, blank=True, null=True)
    def __str__(self):
        return "{0} {1}".format(self.street,self.district.district_name)

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
    images = models.ImageField(blank=True, null=True,upload_to=get_file_path)
    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

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

class RentsManager(models.Manager):

    def createRent(self,flat,user,start,end):
        try:
            obj = self.create(flat=flat,rentor=user,start=start,end=end,status=True,created_at=timezone.now())
        except:
            return None
        Access.objects.create(
            user = user, renta=obj, start=obj.start
        )
        
        return obj

    def confirmRent(self,rent,user):
        obj = self.get(id=rent.id,rentor=user)
        obj.status = True
        obj.save()
    
    def checkAvailability(self,flat):
        pass

    def cancelRent(self,rent,user):
        obj = self.get(id=rent.id,rentor=user)
        obj.status = None
        obj.save()
    
    def GetRentedCalendar(self,current_flat):
        if current_flat is None:
            return []
        rented = self.filter(Q(start__gte=timezone.now()) | Q(start__lte=timezone.now(), end__gte=timezone.now()),flat=current_flat,status=True)
        if len(rented) < 1:
            return []
        disabledDates = []
        for i in rented:
            for x in range(int((i.end-i.start).days)+1):
                disabledDates.append(str((i.start+ timedelta(days=x)).date()))
        return disabledDates
    
    def RentedObjects(self,start,end,current_flat):
        rented = Rents.objects.filter(Q(start__gte=start) | Q(start__lte=start, end__gte=end),flat=current_flat,status=True).count()
        if rented > 0:
            return True
        return False

class Rents(models.Model):
    flat = models.ForeignKey(Flats, on_delete=models.CASCADE,related_name="Квартира",related_query_name="Квартира")
    rentor = models.ForeignKey(User, models.DO_NOTHING)
    start = models.DateTimeField(verbose_name='Начало аренды')
    end = models.DateTimeField(verbose_name='Окончание аренды')
    status = models.BooleanField(null=True,default=False)
    paid = models.BooleanField(null=True,default=False)
    created_at = models.DateTimeField(null=True,default=False)
    renta = RentsManager()
    objects = models.Manager()
    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'
        ordering = ['-start']

    def __str__(self):
        return "{0} с {1} по {2}".format(self.flat,self.start,self.end)
    
    def Location(self):
        return self.flat

    def startDate(self):
        return str(self.start)

    def endDate(self):
        return str(self.end)

    def getAlreardyRended(self):
        return self.filter(Q(start__gte=timezone.now()) | Q(start__lte=timezone.now(), end__gte=timezone.now()))

    def AccessObj(self):
        return Access.objects.filter(renta=self.id,user=self.rentor).last()

    def getDays(self):
        days = (self.end-self.start).days
        if days < 1:
            return 1
        return days

    def getPrice(self):
        return self.getDays() * self.flat.price

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.checkDates():
                super().save(*args, **kwargs)
        else:
            print(self.checkDates())
            if self.checkDates():
                days, hours = self.prolongRent()
                if days >= 0 or hours >= 0:
                    super().save(*args, **kwargs)

    def checkDates(self):
        if self.end < self.start:
            print("here 1")
            return False
        if self.start.date() < timezone.now().date():
            print("here 2")
            return False
        if self.getAvailableHours() is not None:
            if self.start < self.getAvailableHours() and self.status is not None:
                print("here 3")
                return False
        rented = Rents.objects.filter(Q(start__gte=self.start) | Q(start__lte=self.start, end__gte=self.end),flat=self.flat,status=True).exclude(id=self.id).count()
        if rented > 0 and self.status is not None:
            print("here 4")
            return False
        return True

    def prolongRent(self):
        date = Rents.objects.filter(start__gte=self.end,flat=self.flat,status=True).first()
        if date is not None:
            return self.dur(date.start - self.end-timedelta(hours=self.flat.cleaning_time.hour,minutes=self.flat.cleaning_time.minute))
        return self.dur(timedelta(days=100))
    
    def dur(self,duration):
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        return days, hours

    def getAvailableHours(self):
        lastRent = Rents.objects.filter(status=True,flat=self.flat).exclude(id=self.id).last()
        if lastRent is not None:
            return lastRent.end + timedelta(hours=self.flat.cleaning_time.hour,minutes=self.flat.cleaning_time.minute)
        return None


class Payments(models.Model):
    P_TYPES = (
        ('P', 'Подтверждение аккаунта'),
        ('D', 'Депозит'),
        ('F', 'Полная стоимость')
    )
    PAID_TYPES = (
        (False, 'Не оплачен'),
        (True, 'Оплачен')
    )
    rentor = models.ForeignKey(User, models.DO_NOTHING)
    renta = models.ForeignKey(Rents, on_delete=models.CASCADE,blank=True, null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateTimeField()
    status = models.BooleanField(null=True,default=False,choices=PAID_TYPES)
    payment_type = models.CharField(blank=True, null=True,choices=P_TYPES,default='D',max_length=1)
    payment_id = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(null=True,blank=True)
    expires_at = models.DateTimeField(null=True,blank=True)
    captured_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name = 'Транзакция Yandex'
        verbose_name_plural = 'Транзакции Yandex'

class SystemLogs(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING,blank=True, null=True)
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE,blank=True, null=True)
    worker = models.ForeignKey(Workers, on_delete=models.CASCADE,blank=True, null=True)
    district = models.ForeignKey(Districts, on_delete=models.CASCADE,blank=True, null=True)
    flat = models.ForeignKey(Flats, on_delete=models.CASCADE,blank=True, null=True)
    payment = models.ForeignKey(Payments, on_delete=models.CASCADE,blank=True, null=True)
    rents = models.ForeignKey(Rents, on_delete=models.CASCADE,blank=True, null=True)

class Access(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING,blank=True, null=True)
    renta = models.ForeignKey(Rents, on_delete=models.CASCADE,blank=True, null=True)
    start = models.DateTimeField('Start',blank=True, null=True)
    end = models.DateTimeField('End',blank=True, null=True)
    used = models.IntegerField(blank=True, null=True,default=0)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('sharing:access', args=[int(self.pk)])

    def CheckAccess(self):
        if self.end is not None:
            now = timezone.now()
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
                self.save()
        return False

    def timeRemaining(self):
        if self.end is not None:
            now = timezone.now()
            if (now > self.start) and (now < self.end):
                return "{0} осталось".format(str(self.end - now))
            else:
                if (now < self.start):
                    return "Доступна с {0}".format(self.start.strftime("%b %d %Y %H:%M:%S"))
                return "[Не доступно]"
        else:
            return "10 минут осталось"

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
    phone_number = models.CharField(max_length=50,default="", blank=False, null=False,verbose_name="Мобильный номер")
    image_one = models.ImageField(upload_to=get_file_path_users,default=None,verbose_name="Фотография первой страницы паспорта")
    image_two = models.ImageField(upload_to=get_file_path_users,default=None,verbose_name="Фотография страницы с пропиской")
    status = models.BooleanField(null=False,default=False,choices=PAID_TYPES)
    yakey = models.CharField(max_length=50,default=None, blank=False, null=True)
    totlal_cancelation = models.IntegerField(null=True,default=0,blank=True)    

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Документы пользователей'
        verbose_name_plural = 'Документы пользователей'
    



    













