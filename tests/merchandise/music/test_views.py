import pytest

from django.core.urlresolvers import reverse

from components.merchandise.music import factories


@pytest.mark.django_db
def test_album_detail_view(client):
    album = factories.AlbumFactory()
    response = client.get(reverse('album-detail', kwargs={'slug': album.slug}))
    assert response.status_code == 200
    assert 'object' in response.context
    assert 'merchandise/music/album_detail.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_single_detail_view(client):
    single = factories.SingleFactory()
    response = client.get(reverse('single-detail', kwargs={'slug': single.slug}))
    assert response.status_code == 200
    assert 'object' in response.context
    assert 'merchandise/music/single_detail.html' in [template.name for template in response.templates]
