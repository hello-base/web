from django import forms

from . import models


class ShopForm(forms.ModelForm):
    class Meta:
        model = models.Shop


class GoodForm(forms.ModelForm):
    class Meta:
        model = models.Good


class SetForm(forms.ModelForm):
    class Meta:
        model = models.Set


class SuperSetForm(forms.ModelForm):
    class Meta:
        model = models.SuperSet
