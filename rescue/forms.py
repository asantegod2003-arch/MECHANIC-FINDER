from django import forms
from .models import RescueRequest


class RescueRequestForm(forms.ModelForm):

    class Meta:
        model = RescueRequest

        fields = [
            "vehicle_problem",
            "location",
            "phone_number",
            "customer_latitude",
            "customer_longitude",
        ]

        widgets = {
            "vehicle_problem": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Flat tyre, Engine won't start",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Town, landmark or street",
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 0241234567",
                }
            ),

            "customer_latitude": forms.HiddenInput(),
            "customer_longitude": forms.HiddenInput(),
        }