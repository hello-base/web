# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from django.db import models


class ReleaseManager(models.Manager):
    def get_query_set(self):
        return super(ReleaseManager, self).get_query_set().prefetch_related('editions__order__track')


class AlbumManager(ReleaseManager):
    pass


class SingleManager(ReleaseManager):
    pass


class EditionManager(models.Manager):
    def get_query_set(self):
        return super(EditionManager, self).get_query_set().prefetch_related('order')


class TrackOrderManager(models.Manager):
    def get_query_set(self):
        return super(TrackOrderManager, self).get_query_set().prefetch_related('track')


class VideoTrackOrderManager(models.Manager):
    def get_query_set(self):
        return super(VideoTrackOrderManager, self).get_query_set().prefetch_related('video')
