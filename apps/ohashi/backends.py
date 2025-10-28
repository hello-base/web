from django.conf import settings
from django.contrib.staticfiles.storage import CachedFilesMixin

from boto.utils import parse_ts
from storages.backends.s3boto import S3BotoStorage


class CachedStaticS3Storage(CachedFilesMixin, S3BotoStorage):
    """
    A storage class that allows for the speification of a second S3 bucket
    (in this case to give static media its own location), while also
    giving it the same post-processing functionality that Django's cached
    storage supplies.

    """
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = getattr(settings, 'STATIC_STORAGE_BUCKET_NAME')
        super(CachedStaticS3Storage, self).__init__(*args, **kwargs)

    def modified_time(self, name):
        name = self._normalize_name(self._clean_name(name))
        entry = self.entries.get(name)
        if entry is None:
            entry = self.bucket.get_key(self._encode_name(name))
        # Parse the last_modified string to a local datetime object.
        return parse_ts(entry.last_modified)
