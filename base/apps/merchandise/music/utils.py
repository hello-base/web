# -*- coding: utf-8 -*-
def get_previous_release(release, release_type):
    if release.number:
        try:
            obj = filter(None, [release.groups.all(), release.idols.all()])[0].get()
            qs = getattr(obj, release_type).order_by('-released').exclude(number='')
            return qs.filter(released__lt=release.released)[0]
        except IndexError:
            return None


def get_next_release(release, release_type):
    if release.number:
        try:
            obj = filter(None, [release.groups.all(), release.idols.all()])[0].get()
            qs = getattr(obj, release_type).order_by('released').exclude(number='')
            return qs.filter(released__gt=release.released)[0]
        except IndexError:
            return None
