from django import forms
from sharing.models import UsersDocuments

class UserDocumentsForm(forms.ModelForm):

    class Meta:
        #exclude = ('user',)
        fields = ('firstname','lastname','phone_number','image_one','image_two','agreement')
        model = UsersDocuments