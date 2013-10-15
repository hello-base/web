import pytest

from components.merchandise.music.models import Album, Single
from components.merchandise.music.factories import (AlbumFactory,
    BaseFactory, SingleFactory)


@pytest.mark.django_db
def test_album_factory():
    factory = AlbumFactory()
    assert isinstance(factory, Album)
    assert 'album' in factory.romanized_name
    assert factory.identifier == 'album'


@pytest.mark.django_db
def test_single_factory():
    factory = SingleFactory()
    assert isinstance(factory, Single)
    assert 'single' in factory.romanized_name
    assert factory.identifier == 'single'
