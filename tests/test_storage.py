from components.storage import (MediaFilesStorage, StaticFilesStorage,
    S3ManifestStorage)


def test_mediafilesstorage(settings):
    assert MediaFilesStorage()


def test_staticfilesstorage(settings):
    assert StaticFilesStorage()


def test_s3manifeststorage(settings):
    assert S3ManifestStorage()
