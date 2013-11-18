# -*- coding: utf-8 -*-
from datetime import date

from django.db.models.query import QuerySet


class CorrelationQuerySet(QuerySet):
    def today(self):
        return self.filter(julian=date.today().timetuple().tm_yday)
