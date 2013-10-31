import datetime

from django.template import Template, Context


def test_age():
    birthdate = datetime.date.today() - datetime.timedelta(days=731)
    out = Template(
        '{% load people_tags %}'
        '{{ birthdate|age }}'
    ).render(Context({'birthdate': birthdate}))
    assert out == '2'
