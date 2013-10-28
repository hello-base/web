import urlparse

from django.conf import settings

from ecstatic.storage import CachedStaticFilesMixin, StaticManifestMixin
from s3_folder_storage.s3 import DefaultStorage, StaticStorage


def domain(url):
    return urlparse.urlparse(url).hostname


class MediaFilesStorage(DefaultStorage):
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = settings.AWS_STORAGE_BUCKET_NAME
        kwargs['custom_domain'] = domain(settings.MEDIA_URL)
        super(MediaFilesStorage, self).__init__(*args, **kwargs)


class StaticFilesStorage(StaticStorage):
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = settings.AWS_STORAGE_BUCKET_NAME
        kwargs['custom_domain'] = domain(settings.STATIC_URL)
        super(StaticFilesStorage, self).__init__(*args, **kwargs)


class S3ManifestStorage(StaticManifestMixin, CachedStaticFilesMixin, StaticFilesStorage):
    pass
