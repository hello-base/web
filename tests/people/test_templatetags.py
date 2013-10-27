import datetime

from django.template import Template, Context

from components.people.templatetags.people_tags import age


def test_age():
    birthdate = datetime.date.today() - datetime.timedelta(days=731)
    out = Template(
        "{% load people_tags %}"
        "{{ birthdate|age }}"
    ).render(Context({'birthdate': birthdate}))
    assert out == '2'
