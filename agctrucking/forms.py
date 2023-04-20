from django import forms
from django.forms import ModelForm
from .models import *
from django.forms import DateInput


class AgcTruckingForm(ModelForm):
    class Meta:
        model = order_data

        fields = (
            "sopnumbe",
            "projectedshipdate",
            "requesteddeliverydate",
            "truckingconfirmed",
            "shippingcontact",
            "correspondencenotes",
            "shipped",
        )

        widgets = {
            "sopnumbe": forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "projectedshipdate": forms.DateInput(attrs={"type": "date"}),
            "requesteddeliverydate": forms.DateInput(attrs={"type": "date"}),
            "truckingconfirmed": forms.CheckboxInput(),
            "shippingcontact": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "shippingcontact",
                }
            ),
            "correspondencenotes": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "correspondencenotes"}
            ),
            "shipped": forms.CheckboxInput(),
        }
