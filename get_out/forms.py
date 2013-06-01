from django import forms

class LocationSearchForm(forms.Form):
    location = forms.CharField(max_length=100, initial="Wilsons Promontory")

