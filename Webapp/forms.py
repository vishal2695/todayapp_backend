from django import forms
from .models import *



class userloginfrm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'ggg'}),error_messages={'required':'Enter Username'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'ggg'}),error_messages={'required':'Enter Password'})

    # def clean_username(self):
    #     uname = self.cleaned_data['username']
    #     if not Master.objects.filter(username=uname):
    #         raise forms.ValidationError('Invalid Username')
    #     return uname
