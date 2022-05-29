from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Category, Post


@receiver(m2m_changed, sender=Post.postCategories.through)
def notify_users_post(sender, instance, **kwargs):
    send_mail(instance)


#@receiver(post_save, sender=Category)
#def notify_users_post(sender, instance, created, **kwargs):
#    if created:
#        subject = f'New post in {instance.article_text}'
#    else:
#        subject = f'Post changed for{instance.article_text}'
#
#    send_mail(
#        subject = subject,
#        message = instance.message,
#    )