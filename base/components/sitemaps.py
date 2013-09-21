from django.contrib.sitemaps import Sitemap

from merchandise.music.models import Album, Single
from people.constants import STATUS
from people.models import Group, Idol


class AlbumSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Album.objects.all()

    def lastmod(self, obj):
        return obj.modified


class GroupSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return Group.objects.all()

    def lastmod(self, obj):
        return obj.modified

    def priority(self, obj):
        if obj.status == STATUS.active:
            return 0.75
        return 0.5


class IdolSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return Idol.objects.all()

    def lastmod(self, obj):
        return obj.modified

    def priority(self, obj):
        if obj.status == STATUS.active:
            return 0.75
        return 0.5


class SingleSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Single.objects.all()

    def lastmod(self, obj):
        return obj.modified
