import os
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete, post_init, post_save
from django.dispatch import receiver


def profile_picture_path(instance, filename):
    return 'profile/{0}{1}'.format(
        str(uuid.uuid4()),
        os.path.splitext(filename)[1])


class User(AbstractUser):
    bio = models.TextField(blank=True, max_length=500)
    email_verified = models.BooleanField(default=False)
    picture = models.ImageField(_("Profile Picture"),
                                upload_to=profile_picture_path, blank=True)
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username

# Following function help to delete images physically from disk after removal


@receiver(post_delete, sender=User)
def user_delete(sender, instance, **kwargs):
    instance.picture.delete(False)


@receiver(post_init, sender=User)
def clear_picture(sender, instance, **kwargs):
    if instance.picture:
        instance.__ptd = instance.picture


@receiver(post_save, sender=User)
def clear_picture2(sender, instance, **kwargs):
    if hasattr(instance, '__ptd'):
        if not instance.picture or instance.__ptd.path != instance.picture.path:
            instance.__ptd.delete(save=False)
