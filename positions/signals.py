from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Test
# from .tasks import create_all_codes

# @receiver(post_save, sender=Test)
# def set_codes(sender, instance, created, *args, **kwargs):
#     if created:
#         create_all_codes.delay()