from django import forms

class PriceFilterForm(forms.Form):
    price_Min = forms.IntegerField(required=False)
    price_Max = forms.IntegerField(required=False)
    brand = forms.CharField(required=False)