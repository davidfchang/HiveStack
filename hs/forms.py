# -*- coding:latin
from django import forms


__author__ = 'David'



class RegistrationForm(forms.Form):
    #user = models.ForeignKey(User, unique = True, related_name = 'user')
    username = forms.CharField(max_length=20, label="Username", required=True)
    first_name = forms.CharField(max_length=50, label="First Name", required=True)
    middle_name = forms.CharField(max_length=50, label="Middle Name", required=True)
    last_name = forms.CharField(max_length=50, label="Last Name", required=True)
    company_name = forms.CharField(max_length=50, label="Company (optional)", required=False)
    email = forms.EmailField(max_length=80, label="Email", required=True)
    birthday = forms.DateField(label="Birth Date", required=True) # underage users can't work on nsfw projects
    phone_number = forms.CharField(label="Phone Number", required=True, max_length=50)

    city = forms.CharField(max_length=50, label="City", required=True)
    country = forms.CharField(max_length=50, label="Country", required=True)

    password = forms.CharField(max_length=40, widget=forms.PasswordInput,label="Password",required=True)
    repeat_password = forms.CharField(max_length=40, widget=forms.PasswordInput,label="Password",required=True)