from django.core.urlresolvers import reverse


def test_site_view(client):
    response = client.get(reverse('site-home'))
    assert response.status_code == 200
    assert 'landings/home_site.html' in [template.name for template in response.templates]


def test_plain_text_view(client):
    response = client.get(reverse('humans'))
    assert response.status_code == 200
    assert 'humans.txt' in [template.name for template in response.templates]


def test_xml_view(client):
    response = client.get(reverse('opensearch'))
    assert response.status_code == 200
    assert 'opensearch.xml' in [template.name for template in response.templates]
