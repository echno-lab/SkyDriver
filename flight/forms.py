from django import forms

CLASS_CHOICES = [("ECONOMY", "Economy"), ("BUSINESS", "Business")]
ADULTS = [(1, "1 Adult"), (2, "2 Adults"), (3, "3 Adults"), (4, "4 Adults")]


class FlightSearchForm(forms.Form):
    origin = forms.CharField(widget=forms.TextInput(attrs={"list": "origin_list"}))
    destination = forms.CharField(widget=forms.TextInput(attrs={"list": "destination_list"}))
    departure_date = forms.DateField(
        label="Departure",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    return_date = forms.DateField(label="Return", widget=forms.DateInput(attrs={"type": "date"}))
    adults = forms.ChoiceField(
        label="Adults", choices=ADULTS, widget=forms.Select(attrs={"class": "border rounded"})
    )
    class_type = forms.ChoiceField(
        choices=CLASS_CHOICES, widget=forms.Select(attrs={"class": "border rounded"})
    )
