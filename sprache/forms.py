from django import forms
from sprache.models import UserAccount
class UserDocumentsForm(forms.ModelForm):
    class Meta:
        #exclude = ('user',)
        fields = ('email','first_name','last_name','price',)
        model = UserAccount