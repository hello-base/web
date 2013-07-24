import floppyforms as forms
from django.forms.models import inlineformset_factory

from .models import Event, Performance, Venue


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        widgets = {
            'end_date': forms.DateInput,
            'info_link': forms.URLInput,
            'start_date': forms.DateInput,
        }


class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        widgets = {
            'day': forms.DateInput,
            'end_time': forms.TimeInput,
            'start_time': forms.TimeInput,
        }
PerformanceFormset = inlineformset_factory(Event, Performance, form=PerformanceForm)


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
