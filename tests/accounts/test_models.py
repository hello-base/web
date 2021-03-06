# -*- coding: utf-8 -*-
import pytest

from django.core import mail

from apps.accounts.factories import EditorFactory
from apps.accounts.models import Editor

pytestmark = pytest.mark.django_db


class TestEditors:
    def test_factory(self):
        factory = EditorFactory()
        assert isinstance(factory, Editor)
        assert 'dancer' in factory.username

    def test_failing_creation(self):
        with pytest.raises(ValueError):
            Editor.objects.create_user(username='')

    def test_get_full_name(self):
        factory = EditorFactory(username='bryan', name='Bryan')
        assert factory.get_full_name() == 'Bryan'

    def test_get_short_name(self):
        factory = EditorFactory(username='bryan', name='Bryan')
        assert factory.get_short_name() == 'Bryan'

    def test_has_perm(self):
        staff = EditorFactory(username='bryan', is_active=True, is_staff=True)
        assert staff.has_perm('test-perm')

        notstaff = EditorFactory(username='ravyn', is_active=True)
        assert not notstaff.has_perm('test-perm')

    def test_has_module_perms(self):
        staff = EditorFactory(username='bryan', is_active=True, is_staff=True)
        assert staff.has_module_perms('testapp')

        notstaff = EditorFactory(username='ravyn', is_active=True)
        assert not notstaff.has_module_perms('testapp')

    def test_email_user(self):
        factory = EditorFactory(email='to@example.com')
        factory.email_user('Subject', 'Hello there.', from_email='from@example.com')
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == 'Subject'
