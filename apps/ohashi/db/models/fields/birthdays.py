"""
A helper library for Django to work with birthdays in models.

"""
from django.core.exceptions import FieldError
from django.db.models.fields import PositiveSmallIntegerField, DateField
from django.db.models.signals import pre_save


def pre_save_listener(instance, **kwargs):
    field = instance._meta.birthday_field
    birthday = getattr(instance, field.name)
    if not birthday:
        return
    doy = birthday.timetuple().tm_yday
    setattr(instance, field.doy_name, doy)


# An un-editable internal field that will hold the cooresponding day-of-the-
# month for the given date.
internal_field = PositiveSmallIntegerField(editable=False, default=None, null=True)


class BirthdayField(DateField):
    def contribute_to_class(self, cls, name):
        super(BirthdayField, self).contribute_to_class(cls, name)
        if hasattr(cls._meta, 'birthday_field'):
            raise FieldError('Multiple BirthdayFields are not supported on a single model.')
        cls._meta.birthday_field = self
        self.doy_name = '%s_dayofyear' % name
        internal_field.contribute_to_class(cls, self.doy_name)
        pre_save.connect(pre_save_listener, sender=cls)
