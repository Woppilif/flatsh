from django import forms
from .models import Rents, UsersDocuments, Flats, Images
from django.contrib.admin import widgets 

from django.utils import timezone
from datetime import timedelta,datetime
from django.db.models import Q
from bootstrap_datepicker_plus import DatePickerInput

class UserDocumentsForm(forms.ModelForm):

    class Meta:
        #exclude = ('user',)
        fields = ('firstname','lastname','phone_number','image_one','image_two','agreement')
        model = UsersDocuments

class FlatEditForm(forms.ModelForm):
    def __init__(self,current_user = None , *args, **kwargs):
        super(FlatEditForm, self).__init__(*args, **kwargs)
        print(current_user)
        self.fields['district'].queryset = self.fields['district'].queryset.filter(partner=current_user.workers.partner)

    class Meta:
        fields = '__all__'
        model = Flats  

class FlatImagesForm(forms.ModelForm):
    def __init__(self,current_user = None , *args, **kwargs):
        super(FlatImagesForm, self).__init__(*args, **kwargs)
        #print(current_user)
        #self.fields['district'].queryset = self.fields['district'].queryset.filter(partner=current_user.workers.partner)

    class Meta:
        fields = ('images',)
        model = Images  

class RentForm(forms.ModelForm):
    
    def __init__(self, current_flat = None, *args, **kwargs):
        super(RentForm, self).__init__(*args, **kwargs)
        self.current_flat = current_flat
        self.disabledDates = Rents.renta.GetRentedCalendar(self.current_flat)
        time = timezone.now()
        '''
        self.fields['start'] = forms.DateTimeField(
            input_formats=['%Y-%m-%d %H:%M'],
            widget=XDSoftDateTimePickerInput(
                attrs={'disabledDates':self.disabledDates,'minDate':time.date(),'allowTimes':'14:00'}
                ),label='Начало аренды')
        
   
        
        self.fields['end'] = forms.DateTimeField(
            input_formats=['%Y-%m-%d %H:%M'],
            widget=XDSoftDateTimePickerInput(
                attrs={'disabledDates':self.disabledDates,'minDate':time.date(),'allowTimes':'11:00'})
                ,label='Окончание аренды')
        '''
        
  
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