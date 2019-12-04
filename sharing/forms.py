from django import forms
from .models import Rents, UsersDocuments, Flats, Images
from django.contrib.admin import widgets 
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
    