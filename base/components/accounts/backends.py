from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class HelloBaseIDBackend(ModelBackend):
    def authenticate(self, username=None):
        try:
            user = User.objects.filter(username=username)[0]
        except IndexError:
            return None
        else:
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
