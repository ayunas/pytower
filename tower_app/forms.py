from django import forms

class CreateCharacter(forms.Form):
    name = forms.CharField(label="Name", max_length=100)

class MoveCharacter(forms.Form):
    btn = forms.CharField()
    
class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=32
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )
