from django import forms
from sharing.models import Rents
from django.contrib.admin import widgets 
from .widgets import XDSoftDateTimePickerInput
from django.utils import timezone
from datetime import timedelta,datetime
from django.db.models import Q
# Create your models here.

class RentForm(forms.ModelForm):
    
    def __init__(self, current_flat = None, *args, **kwargs):
        super(RentForm, self).__init__(*args, **kwargs)
        self.current_flat = current_flat
        self.disabledDates = Rents.renta.GetRentedCalendar(self.current_flat)
        time = timezone.now()
        
        self.fields['start'] = forms.DateTimeField(
            input_formats=['%Y-%m-%d %H:%M'],
            widget=XDSoftDateTimePickerInput(
                attrs={'disabledDates':self.disabledDates,'minDate':time.date(),'allowTimes':'14:00'}
                ),label='Начало аренды')
        
        #,'minTime':time.time()
        
        self.fields['end'] = forms.DateTimeField(
            input_formats=['%Y-%m-%d %H:%M'],
            widget=XDSoftDateTimePickerInput(
                attrs={'disabledDates':self.disabledDates,'minDate':time.date(),'allowTimes':'11:00'})
                ,label='Окончание аренды')
        
  
    class Meta:
        fields = ('start','end')
        model = Rents  

    def clean(self):
        cd = self.cleaned_data
        if str(cd.get('start').time()) != "14:00:00":
            self.add_error('start', "Время не может быть неравно 14:00")

        if str(cd.get('end').time()) != "11:00:00":
            self.add_error('start', "Время не может быть неравно 11:00")

        if cd.get('end') < cd.get('start'):
            self.add_error('end', "Дата окончания аренды не может быть меньше даты начала аренды")

        if Rents.renta.RentedObjects(cd.get('start'),cd.get('end'),self.current_flat):
            self.add_error('start', "Данная дата уже занята")
            self.add_error('end', "Данная дата уже занята")

class RentFormEx(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(RentFormEx, self).__init__(*args, **kwargs)
        time = timezone.now()
        
        self.fields['start'] = forms.DateTimeField(
            input_formats=['%Y-%m-%d %H:%M'],
            widget=XDSoftDateTimePickerInput(
                attrs={'minDate':time.date(),'allowTimes':'14:00'}
                ),label='Начало аренды')
        
        #,'minTime':time.time()
        
        self.fields['end'] = forms.DateTimeField(
            input_formats=['%Y-%m-%d %H:%M'],
            widget=XDSoftDateTimePickerInput(
                attrs={'minDate':time.date(),'allowTimes':'11:00'})
                ,label='Окончание аренды')
        
  
    class Meta:
        fields = ('flat','start','end')
        model = Rents  

    def clean(self):
        cd = self.cleaned_data
        if str(cd.get('start').time()) != "14:00:00":
            self.add_error('start', "Время не может быть неравно 14:00")

        if str(cd.get('end').time()) != "11:00:00":
            self.add_error('start', "Время не может быть неравно 11:00")

        if cd.get('end') < cd.get('start'):
            self.add_error('end', "Дата окончания аренды не может быть меньше даты начала аренды")
