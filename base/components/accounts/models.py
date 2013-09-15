from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core import validators
from django.core.urlresolvers import reverse
from django.utils import timezone

from ohashi.db import models

class EditorManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        now = timezone.now()
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


# TODO: Inherit from a custom user class of some kind.
# Maybe that should be in here? The only form of users we have on Base
# ARE editors... I think.
class Editor(AbstractBaseUser):
    username = models.CharField(blank=True, db_index=True)
    name = models.CharField(blank=True)
    email = models.EmailField(db_index=True, unique=True)
    started = models.DateTimeField(default=timezone.now)
    active_sicne = models.DateTimeField(blank=True, default=timezone.now())

    # Authentication-/Authorization-related fields.
    oauth_token = models.CharField(max_length=200, blank=True)


class ContributorMixin(models.Model):
    submitted_by = models.ForeignKey(Editor, related_name='submissions')
    edited_by = models.ManyToManyField(Editor, related_name='edits')

    class Meta:
        abstract = True
