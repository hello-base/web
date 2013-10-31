from datetime import date, timedelta

from django.db.models import get_model


def calculate_age(birthdate, target=None):
    if not target:
        target = date.today()
    birthday = birthdate.replace(year=target.year)
    if birthday > target:
        return target.year - birthdate.year - 1
    else:
        return target.year - birthdate.year


def calculate_average_age(birthdates):
    age_timedelta = sum((date.today() - birthdate for birthdate in birthdates), timedelta(0)) / len(birthdates)
    average_age = round(age_timedelta.days / (365.2425), 2)
    return average_age
