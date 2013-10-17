import datetime
import pytest

from components.merchandise.music.models import Album, Single
from components.merchandise.music.factories import (AlbumFactory,
    BaseFactory, SingleFactory)
from components.people.factories import GroupFactory


pytestmark = pytest.mark.django_db

def test_album_factory():
    factory = AlbumFactory()
    assert isinstance(factory, Album)
    assert 'album' in factory.romanized_name
    assert factory.identifier == 'album'


def test_album_get_absolute_url(client):
    factory = AlbumFactory()
    response = client.get(factory.get_absolute_url())
    assert response.status_code == 200


def test_single_factory():
    factory = SingleFactory()
    assert isinstance(factory, Single)
    assert 'single' in factory.romanized_name
    assert factory.identifier == 'single'


def test_single_get_absolute_url(client):
    factory = SingleFactory()
    response = client.get(factory.get_absolute_url())
    assert response.status_code == 200


def test_single_get_previous_and_next():
    single1 = SingleFactory(number='1', romanized_name='single1', released=datetime.date.today() - datetime.timedelta(days=14))
    single2 = SingleFactory(number='2', romanized_name='single2', released=datetime.date.today() - datetime.timedelta(days=7))

    group = GroupFactory()
    single1.groups.add(group)
    assert single1.groups.exists()
    single2.groups.add(group)
    assert single2.groups.exists()

    previous = single2.get_previous
    assert previous == single1

    next = single1.get_next
    assert next == single2
