from django import forms

class EventSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search Events')
