from django import forms

class LocationSearchForm(forms.Form):
    location = forms.CharField(max_length=100, initial="Wilsons Promontory")
    simple_names = forms.BooleanField(initial=True, label='Common names')
