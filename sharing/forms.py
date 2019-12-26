from django import forms
from .models import Rents, UsersDocuments, Flats, Images
from django.contrib.admin import widgets 
from sharing.widgets import XDSoftDateTimePickerInput
from django.utils import timezone
from datetime import timedelta,datetime
from django.db.models import Q


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
    now = timezone.now().replace(hour=14,minute=0,second=0)
    start = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
        fields = ('flat','start','end')
        model = Rents  

    def clean(self):
        cd = self.cleaned_data

class RentFormEx(forms.ModelForm):

    paid = forms.ChoiceField(choices=(
        (True,'Оплачена наличными'),
        (False, 'Оплата картой клиента')
    ))
    
    def __init__(self, *args, **kwargs):
        super(RentFormEx, self).__init__(*args, **kwargs)
        time = timezone.now()
        
        self.fields['start'] = forms.DateTimeField(
            input_formats=['%Y-%m-%d %H:%M'],
            widget=XDSoftDateTimePickerInput(
                attrs={'minDate':time.date(),'allowTimes':'14:00','class':'cal'}
                ),label='Начало аренды')
        
        #,'minTime':time.time()
        
        self.fields['end'] = forms.DateTimeField(
            input_formats=['%Y-%m-%d %H:%M'],
            widget=XDSoftDateTimePickerInput(
                attrs={'minDate':time.date(),'allowTimes':'12:00','class':'cal'})
                ,label='Окончание аренды')
        
  
    class Meta:
        fields = ('flat','start','end','paid')
        model = Rents  

    def clean(self):
        cd = self.cleaned_data
        if str(cd.get('start').time()) != "14:00:00":
            self.add_error('start', "Время не может быть неравно 14:00")

        if str(cd.get('end').time()) != "12:00:00":
            self.add_error('start', "Время не может быть неравно 12:00")

        if cd.get('end') < cd.get('start'):
            self.add_error('end', "Дата окончания аренды не может быть меньше даты начала аренды")
    