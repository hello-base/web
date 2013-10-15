import pytest

from components.merchandise.music.models import Album, Single
from components.merchandise.music.factories import (AlbumFactory,
    BaseFactory, SingleFactory)


@pytest.mark.django_db
class TestAlbums(object):
    def test_album_factory(self):
        album = AlbumFactory()
        assert isinstance(album, Album)
        assert 'album' in album.romanized_name
        assert album.identifier == 'album'


@pytest.mark.django_db
class TestSingles(object):
    def test_single_factory(self):
        single = SingleFactory()
        assert isinstance(single, Single)
        assert 'single' in single.romanized_name
        assert single.identifier == 'single'
