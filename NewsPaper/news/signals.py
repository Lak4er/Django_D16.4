from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post


@receiver(m2m_changed, sender=Post.categories.through, dispatch_uid='notify_post_created_signal')
def notify_post(sender, instance, action, **kwargs):
    if action == 'post_add':
        senders = []
        for category in instance.categories.all():
            for subscriber in category.subscribers_categoty.all():
                senders.append(subscriber.email)

        html_content = render_to_string('email.html', {'post': instance})
        msg = EmailMultiAlternatives(
            subject=f'{instance}',
            body='',
            from_email='',
            to=senders
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
