from django import forms

class CreateCharacter(forms.Form):
    name = forms.CharField(label="Name", max_length=100)