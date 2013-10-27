import datetime

from components.people.utils import calculate_age, calculate_average_age


def test_calculate_age():
    birthdate = datetime.date.today() - datetime.timedelta(days=731)
    target = datetime.date.today() - datetime.timedelta(days=365)
    assert calculate_age(birthdate) == 2
    assert calculate_age(birthdate, target) == 1


def test_cacluate_average_age():
    birthdates = [
        datetime.date.today() - datetime.timedelta(days=731),
        datetime.date.today() - datetime.timedelta(days=366)
    ]
    assert calculate_average_age(birthdates) == 1.5
