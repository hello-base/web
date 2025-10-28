from django import forms
from django.core import exceptions
from django.db import models, router
from django.db.models import Field, ForeignKey


class CharField(Field):
    def formfield(self, **kwargs):
        defaults = {'widget': forms.TextInput}
        defaults.update(kwargs)
        return super(CharField, self).formfield(**defaults)

    def db_type(self, connection):
        if self.max_length:
            return 'varchar(%s)' % self.max_length
        return 'text'


class EmailField(CharField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.EmailField}
        defaults.update(kwargs)
        return super(EmailField, self).formfield(**defaults)


class SlugField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('db_index', True)
        super(SlugField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.SlugField}
        defaults.update(kwargs)
        return super(SlugField, self).formfield(**defaults)


class URLField(CharField):
    def __init__(self, verbose_name=None, name=None, **kwargs):
        super(URLField, self).__init__(verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.URLField}
        defaults.update(kwargs)
        return super(URLField, self).formfield(**defaults)


class CustomManagerForeignKey(ForeignKey):
    """
    Inspired by:
    <http://www.hoboes.com/Mimsy/hacks/custom-managers-django-foreignkeys/>

    """
    def __init__(self, *args, **kwargs):
        if 'manager' in kwargs:
            self.custom_manager = kwargs['manager']()
            del kwargs['manager']
        else:
            self.custom_manager = None
        super(CustomManagerForeignKey, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        field = super(CustomManagerForeignKey, self).formfield(**kwargs)
        if self.custom_manager:
            field.queryset = self.custom_manager
        return field

    def validate(self, value, model_instance):
        if self.rel.parent_link:
            return
        super(models.ForeignKey, self).validate(value, model_instance)
        if value is None:
            return
        if self.custom_manager:
            manager = self.custom_manager
        else:
            using = router.db_for_read(model_instance.__class__, instance=model_instance)
            manager = self.rel.to._default_manager.using(using)
        qs = manager.filter(**{self.rel.field_name: value})
        qs = qs.complex_filter(self.rel.limit_choices_to)
        if not qs.exists():
            raise exceptions.ValidationError(
                self.error_messages['invalid'] % {
                    'model': self.rel.to._meta.verbose_name,
                    'pk': value
                }
            )
