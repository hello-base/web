from django.core.files.base import ContentFile

from ecstatic.storage import CachedStaticFilesMixin, StaticManifestMixin
from s3_folder_storage.s3 import StaticStorage


class S3ManifestStorage(StaticManifestMixin, CachedStaticFilesMixin, StaticStorage):
    pass
