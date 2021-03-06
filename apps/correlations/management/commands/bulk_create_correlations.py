# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand

from apps.correlations.models import record_correlation
from apps.people.models import Group, Idol, Membership
from apps.merchandise.music.models import Album, Single

QUERYSETS = [
    # apps.people
    Group.objects.all(),
    Idol.objects.all(),
    Membership.objects.all(),

    # apps.music
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
