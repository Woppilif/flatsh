from django import forms
from .models import *
from django.contrib.admin import widgets  

class RentFlatForm(forms.ModelForm):

    class Meta:
        model = Rents
        fields = ('start',)
    def __init__(self, *args, **kwargs):
        super(RentFlatForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget = widgets.AdminSplitDateTime()

class UserDocumentsForm(forms.ModelForm):

    class Meta:
        #exclude = ('user',)
        fields = ('firstname','lastname','phone_number','image_one','image_two','agreement')
        model = UsersDocuments

class RentForm(forms.ModelForm):

    class Meta:
    #exclude = ('user',)
        fields = ('start','end')
        model = Rents  

    def __init__(self, *args, **kwargs):
        super(RentForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget = widgets.AdminSplitDateTime()
        self.fields['end'].widget = widgets.AdminSplitDateTime()

class RentSearchForm(forms.ModelForm):
    start = forms.DateField()
    end = forms.DateField()
    class Meta:
        fields = ('start','end')
        model = Rents  