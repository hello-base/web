# -*- coding: utf-8 -*-
from django.db import models


class EditionManager(models.Manager):
    def regular_edition(self, release=None, edition=None):
        kwargs = {'kind': self.model.EDITIONS.regular}
        if release:
            kwargs[release.identifier] = release
        if edition:
            kwargs[edition.parent.identifier] = edition.parent

        qs = super(EditionManager, self).get_query_set().order_by('released', 'romanized_name')

        try:
            return qs.filter(**kwargs)[0]
        except IndexError:
            return qs.none()
