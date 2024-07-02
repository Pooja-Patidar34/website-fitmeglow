
# Create your models here.
# accounts/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='userprofile'
    )
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    # Add other fields as needed

    def __str__(self):
        return self.user.username  # Customize as needed