from django.contrib.sitemaps import Sitemap

from merchandise.music.models import Album, Single, Track
from people.constants import STATUS
from people.models import Group, Idol


class BaseSitemap(Sitemap):
    changefreq = 'daily'

    def lastmod(self, obj):
        return obj.modified


class AlbumSitemap(BaseSitemap):
    priority = 0.6

    def items(self):
        return Album.objects.all()


class GroupSitemap(BaseSitemap):
    def items(self):
        return Group.objects.all()

    def priority(self, obj):
        if obj.status == STATUS.active:
            return 0.75
        return 0.5


class IdolSitemap(BaseSitemap):
    def items(self):
        return Idol.objects.all()

    def priority(self, obj):
        if obj.status == STATUS.active:
            return 0.75
        return 0.5


class SingleSitemap(BaseSitemap):
    priority = 0.6

    def items(self):
        return Single.objects.all()


class TrackSitemap(BaseSitemap):
    priority = 0.5

    def items(self):
        return Track.objects.originals()
