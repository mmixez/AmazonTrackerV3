from django import forms

class ProductURLForm(forms.Form):
    url = forms.URLField(
    label='Amazon Product URL',
    widget=forms.URLInput(attrs={'placeholder': 'Enter Amazon product URL'}),
    assume_scheme='http'  # or 'https' if you want the new default behavior
)

    target_price = forms.FloatField(label='Target Price (USD)')