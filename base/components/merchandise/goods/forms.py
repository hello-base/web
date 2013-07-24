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


class BaseGoodForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(BaseGoodForm, self).clean()

        # Of course the date a good is available until cannot be earlier than
        # the date it was released.
        available_from = cleaned_data.get('available_from', '')
        available_until = cleaned_data.get('available_until', '')
        if (available_from and available_until) and (available_until < available_from):
            message = u'The "Available Until" date is earlier than "Available From".'
            raise forms.ValidationError(message)

        # Goods must be associated with at least one idol or one group. Raise
        # a ValidationError if none are associated.
        groups = cleaned_data.get('groups', '')
        idols = cleaned_data.get('idols', '')
        if not groups and not idols:
            message = u'Goods must be associated with at least one idol or group.'
            raise forms.ValidationError(message)

        # Goods must originate from either a shop or an event. Raise a
        # ValidationError if neither of them are set.
        event = cleaned_data.get('event', '')
        shop = cleaned_data.get('shop', '')
        if not event and not shop:
            message = u'Goods must either originate from a shop or an event.'
            raise forms.ValidationError(message)

        return cleaned_data


class GoodForm(BaseGoodForm):
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
            'name': forms.TextInput,
            'other_info': forms.Textarea(attrs={'rows': 2}),
            'price': forms.NumberInput,
            'romanized_name': forms.TextInput,
        }


class SetForm(BaseGoodForm):
    class Meta:
        model = models.Set


class SuperSetForm(BaseGoodForm):
    class Meta:
        model = models.SuperSet
