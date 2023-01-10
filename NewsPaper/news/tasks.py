from celery import shared_task
from datetime import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsPaper.NewsPaper.settings import *

from .models import Post, Category

@shared_task
def mail_new():
    post = Post.save(commit=False)
    html_content = render_to_string(
        'email.html',
        {
            'post': post,
            'text': post.preview,
            'link': f'http://127.0.0.1:8000/news/{post.pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'{post.post_title}',
        body=post.post_text,
        from_email=DEFAULT_FROM_EMAIL,
        to=Category.objects.all()
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()

@shared_task
def week_news_notification():
    for category in Category.subscribers_categoty.all():
        senders = []
        for subscriber in category.subscribers_categoty.all():
            senders.append(subscriber.email)

        html_content = render_to_string('email_week.html', {'posts': Post.objects.filter(categories=category).filter(
            time_in_post__lt=datetime.now() - timedelta(days=7))})
        msg = EmailMultiAlternatives(
            subject=f'Список новых статей за прошедшую неделю!',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=senders
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
