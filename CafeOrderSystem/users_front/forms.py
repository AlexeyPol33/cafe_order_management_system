from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.PasswordInput()
    password_repeat = forms.PasswordInput()