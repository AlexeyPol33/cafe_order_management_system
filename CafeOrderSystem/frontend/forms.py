from django import forms


class OrderPostForm(forms.Form):
    table = forms.IntegerField(
        min_value=1,
        max_value=15,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Введите номер столика'
        }),
        )
class SearchForm(forms.Form):
    query = forms.CharField()