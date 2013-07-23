import floppyforms as forms

from . import models

# Good Django decorum requires us to explicitly list out fields. We have a lot
# of fields, so we're splitting them up into common sections:
BASE_GOOD_FIELDS = [
    # Metadata.
    'romanized_name', 'name', 'price',  'online_id', 'other_info',
    'available_from', 'available_until', 'link', 'image',

    # Relations.
    'idols', 'groups', 'event', 'shop',
]


class ShopForm(forms.ModelForm):
    class Meta:
        model = models.Shop


class GoodForm(forms.ModelForm):
    class Meta:
        model = models.Good
        fields = BASE_GOOD_FIELDS + [
            'category', 'parent', 'is_bonus_good', 'is_campaign_good',
            'is_lottery_good', 'is_set_exclusive'
        ]
        widgets = {
            'available_from': forms.DateInput,
            'available_until': forms.DateInput,
            'link': forms.URLInput,
            'price': forms.NumberInput,
        }


class SetForm(forms.ModelForm):
    class Meta:
        model = models.Set


class SuperSetForm(forms.ModelForm):
    class Meta:
        model = models.SuperSet
