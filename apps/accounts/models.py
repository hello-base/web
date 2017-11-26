# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail

from model_utils.models import TimeStampedModel
from ohashi.db import models


class EditorManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        now = datetime.now()
        if not username:
            raise ValueError('The given username must be set.')
        email = EditorManager.normalize_email(email)
        user = self.model(
            username=username, email=email, is_staff=False,
            is_active=True, is_superuser=False, last_login=now,
            started=now, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class Editor(AbstractBaseUser):
    # Model Managers.
    objects = EditorManager()

    base_id = models.IntegerField('Hello! Base ID', db_index=True, unique=True)
    username = models.CharField(blank=True, db_index=True, unique=True)
    name = models.CharField(blank=True)
    email = models.EmailField(db_index=True, unique=True)
    started = models.DateTimeField(default=datetime.now)
    active_since = models.DateTimeField(blank=True, default=datetime.now())

    # Authentication-/Authorization-related fields.
    access_token = models.CharField(blank=True)
    refresh_token = models.CharField(blank=True)
    token_expiration = models.IntegerField(blank=True, null=True)

    # Editor status booleans.
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELS = ['email']

    def __str__(self):
        return u'%s' % (self.username)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        # Active staff have all permissions.
        if self.is_active and self.is_staff:
            return True

    def has_module_perms(self, app_label):
        # Active staff have all permissions.
        if self.is_active and self.is_staff:
            return True

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])


class ContributorMixin(TimeStampedModel):
    submitted_by = models.ForeignKey(Editor, blank=True, null=True, related_name='%(class)s_submissions')
    edited_by = models.ManyToManyField(Editor, blank=True, related_name='%(class)ss_edits')

    class Meta:
        abstract = True
