
from django import forms


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)

    billing_address = forms.CharField(max_length=250)
    billing_city = forms.CharField(max_length=100)
    billing_postcode = forms.CharField(max_length=20)
    billing_country = forms.CharField(max_length=100)

    shipping_address = forms.CharField(max_length=250)
    shipping_city = forms.CharField(max_length=100)
    shipping_postcode = forms.CharField(max_length=20)
    shipping_country = forms.CharField(max_length=100)
