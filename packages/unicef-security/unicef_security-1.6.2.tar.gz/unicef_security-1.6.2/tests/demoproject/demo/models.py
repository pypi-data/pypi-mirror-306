from django.contrib.auth.models import AbstractUser

from unicef_security.models import SecurityMixin


class User(SecurityMixin, AbstractUser):
    class Meta(AbstractUser.Meta):
        app_label = "demo"
