from django.contrib.staticfiles.storage import CachedFilesMixin
from django.core.files.base import ContentFile

from pipeline.storage import PipelineMixin
from s3_folder_storage.s3 import StaticStorage


class S3PipelineStorage(PipelineMixin, CachedFilesMixin, StaticStorage):
    # HACK: The chunks implementation in S3 files appears
    # broken when gzipped!
    def hashed_name(self, name, content=None):
        if content is None:
            content = ContentFile(self.open(name).read(), name=name)
        return super(S3PipelineStorage, self).hashed_name(name, content)
