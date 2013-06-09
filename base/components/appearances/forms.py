from django import forms

from .models import Show, TimeSlot, Episode, Synopsis, Magazine, Issue, IssueImage, CardSet, Card


class ShowForm(forms.ModelForm):
    class Meta:
        model = Show


class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode


class MagazineForm(forms.ModelForm):
    class Meta:
        model = Magazine


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue