from django import forms

from .models import Shop, Good, Set, SuperSet


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop


class GoodForm(forms.ModelForm):
    class Meta:
        model = Good


class SetForm(forms.ModelForm):
    class Meta:
        model = Set

class SuperSetForm(forms.ModelForm):
    class Meta:
        model = SuperSet