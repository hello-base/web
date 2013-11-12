# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.query import QuerySet


class EditionManager(models.Manager):
    def find_edition(self, release, edition, **kwargs):
        if release:
            kwargs[release.identifier] = release
        if edition:
            kwargs[edition.parent.identifier] = edition.parent

        qs = super(EditionManager, self).get_queryset().order_by('released', 'romanized_name')

        try:
            return qs.filter(**kwargs)[0]
        except IndexError:
            return qs.none()

    def digital_edition(self, release=None, edition=None):
        kwargs = {'kind': self.model.EDITIONS.digital}
        return self.find_edition(release, edition, **kwargs)

    def regular_edition(self, release=None, edition=None):
        kwargs = {'kind': self.model.EDITIONS.regular}
        return self.find_edition(release, edition, **kwargs)


class TrackQuerySet(QuerySet):
    def originals(self):
        return self.filter(original_track__isnull=True)


class TrackOrderQuerySet(QuerySet):
    def original_only(self):
        return self.filter(is_instrumental=False)
