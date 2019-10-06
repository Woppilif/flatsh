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
        '''
        if self.instance:
            self.current_flat = self.instance
        if current_flat:
        '''
        self.current_flat = current_flat
        print(self.current_flat)
        self.rented = Rents.objects.filter(Q(start__gte=timezone.now()) | Q(start__lte=timezone.now(), end__gte=timezone.now()),flat=self.current_flat,status=True)
        self.disabledDates = []
        for i in self.rented:
            for x in range(int((i.end-i.start).days)+1):
                self.disabledDates.append(str((i.start+ timedelta(days=x)).date()))
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
        print()
        if str(cd.get('start').time()) != "14:00:00":
            self.add_error('start', "Время не может быть неравно 14:00")

        if str(cd.get('end').time()) != "11:00:00":
            self.add_error('start', "Время не может быть неравно 11:00")

        if cd.get('end') < cd.get('start'):
            self.add_error('end', "Дата окончания аренды не может быть меньше даты начала аренды")
        '''
        if 
        if cd.get('start') is not None:
            if cd.get('start'):
                
        '''
