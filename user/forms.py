from django import forms
from sharing.models import UsersDocuments
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phone_field import PhoneField

class UserDocumentsForm(forms.ModelForm):
    phone_number = PhoneField(help_text='Контактный телефон')
    class Meta:
        #exclude = ('user',)
        fields = ('firstname','lastname','phone_number','image_one','image_two',)
        model = UsersDocuments




class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user