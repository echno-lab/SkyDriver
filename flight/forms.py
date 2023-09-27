from django import forms

from .models import Airport, City


class SearchForm(forms.Form):
    origin = forms.CharField(widget=forms.TextInput(attrs={"list": "origin_list"}))
    destination = forms.CharField(widget=forms.TextInput(attrs={"list": "destination_list"}))
    departure_date = forms.DateField(
        label="Departure", widget=forms.DateInput(attrs={"type": "date"})
    )
    return_date = forms.DateField(label="Return", widget=forms.DateInput(attrs={"type": "date"}))
