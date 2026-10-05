from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User


@receiver(post_save, sender=User)
def verify_superuser_email(sender: type[User], instance: User, created: bool, **kwargs: object) -> None:
    if instance.is_superuser and not instance.is_email_verified:
        User.objects.filter(pk=instance.pk).update(is_email_verified=True)