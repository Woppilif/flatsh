from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
import time
from django.core.mail import send_mail
from sharing.models import UsersDocuments, Rents, Access, Payments
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q

class CustomUserCreationForm(forms.Form):
    #username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    phone = forms.CharField(max_length=31,min_length=10,label='Введите номер телефона',help_text='num')
    email = forms.EmailField(label='Укажите вашу почту',help_text='email')
    
    #password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    #password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    '''
    def clean_username(self):
        username = self.cleaned_data['email'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username
    '''
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Такой Email уже зарегистрирован")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone'].lower()
        r = UsersDocuments.objects.filter(phone_number=phone)
        if r.count():
            raise  ValidationError("Такой номер телефона уже зарегистрирован")
        return phone

    '''
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
 
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
 
        return password2
    '''
    def save(self, commit=True):
        password =  int(time.time())
        user = User.objects.create_user(
            self.cleaned_data['email'],
            self.cleaned_data['email'],
            password
        )
        
        send_mail(
            'Регистрация на EWTM',
            'Ваш пароль: {0}'.format(password),
            'ewtm.info@gmail.com',
            ['{0}'.format(self.cleaned_data['email'])],
            fail_silently=False,
        )
        
        UsersDocuments.objects.create(
            user=user,
            phone_number = self.cleaned_data['phone']
        )
        return user,password

class RentaPayForm(forms.Form):
    def __init__(self,renta = None, *args, **kwargs):
        super(RentaPayForm, self).__init__(*args, **kwargs)
        self.renta = renta

    def is_valid(self):
        if self.renta is not None:
            return True
        return False

    def save(self, commit=True):
        paymentObj, created = Payments.objects.get_or_create(
            rentor = self.renta.rentor,
            renta = self.renta,
            price = 1,
            payment_type = 2,
            status = False,
        )
        paymentObj.setInfo(paymentObj.payPrice()).setStatus().rentaPaid()
        if paymentObj.status is True:
            access, created = Access.access.createPaidAccess(paymentObj.renta)
        return self.renta.id

class RentForm(forms.Form):
    def __init__(self,current_flat = None, rentor = None , *args, **kwargs):
        super(RentForm, self).__init__(*args, **kwargs)
        self.current_flat = current_flat
        self.rentor = rentor

    start = forms.DateTimeField(input_formats=["%Y-%m-%dT%H:%M"])
    end = forms.IntegerField()

    def clean_start(self):
        start = self.cleaned_data['start']
        if start.date() < timezone.now().date():
            raise  ValidationError("Начало аренды не может быть позже сегодняшней даты")
        return start

    def clean_end(self):
        end = int(self.cleaned_data['end'])
        if end < 1:
            raise  ValidationError("Окончание аренды не может быть позже сегодняшней даты")
        print(end)
        return end

    def clean(self):
        print(self.cleaned_data)
        end = self.cleaned_data['start'] + timedelta(days=int(self.cleaned_data['end']))
        end = end.replace(hour=12,minute=0)
        r = Rents.objects.filter(
            start__gte=self.cleaned_data['start'].replace(hour=14,minute=0),
            start__lte=end,
            flat=self.current_flat,status=True)
        if r.count():
            self.add_error('start',"Данные даты уже забронированы.")
            raise  ValidationError("Данные даты уже забронированы.")


    def save(self, commit=True):
        renta = Rents.renta.createRent(
            flat = self.current_flat,
            user = self.rentor,
            start = timezone.make_naive(self.cleaned_data['start'].replace(hour=14,minute=0)),
            end = timezone.make_naive((self.cleaned_data['start'] + timedelta(days=int(self.cleaned_data['end']))).replace(hour=12,minute=0))
        )
        access = Access.access.createAccess(renta)
        return renta

    class Meta:
        fields = ('start','end')
        model = Rents  

class UserDocumentsForm(forms.ModelForm):
    
    class Meta:
        #exclude = ('user',)
        fields = ('firstname','lastname','image_one','image_two',)
        model = UsersDocuments

class UploadFileForm(forms.Form):
    file = forms.FileField()


