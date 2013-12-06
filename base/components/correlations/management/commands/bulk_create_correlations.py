# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand

from components.correlations.models import record_correlation
from components.people.models import Group, Idol, Membership
from components.merchandise.music.models import Album, Single

QUERYSETS = [
    # components.people
    Group.objects.all(),
    Idol.objects.all(),
    Membership.objects.all(),

    # components.music
    Album.objects.all(),
    Single.objects.all(),
]


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        # Manually create the correlations! Don't depend on the save() method
        # since that opens whole cans of worms that we don't want.
        for queryset in QUERYSETS:
            for obj in queryset:
                record_correlation(type(obj), obj)
