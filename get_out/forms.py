from django import forms

class LocationSearchForm(forms.Form):
    location = forms.CharField(max_length=100, initial="Wilsons Promontory")
    fish = forms.BooleanField(required=False, initial=False)
    birds = forms.BooleanField(required=False, initial=True)
    mammals = forms.BooleanField(required=False, initial=True)
    marsupials = forms.BooleanField(required=False, initial=True)
    reptiles = forms.BooleanField(required=False, initial=True)
    plants = forms.BooleanField(required=False, initial=True)
    trees = forms.BooleanField(required=False, initial=True)
    other = forms.BooleanField(required=False, initial=True)
