from django import forms

class InviteForm(forms.Form):
    username = forms.CharField()
