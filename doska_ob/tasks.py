from datetime import timezone
from celery import shared_task
import time
from django.conf import settings
from django.template.loader import render_to_string
import datetime
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import Post, Category
import logging
from protect.models import User

logger = logging.getLogger(__name__)


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i + 1)


@shared_task
def send_email_task(pk):
    post = Post.objects.get(pk=pk)
    header = post.post_header
    users = User.objects.values_list('email', flat=True)
    users = []

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': f'{post.post_header}',
            'link': f'{settings.SITE_URL}/doska_ob/{pk}',
        }
    )
    msg = EmailMultiAlternatives(
        subject=header,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=users,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_send_email_task():
    today = datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(create_time__gte=last_week)
    # categories = set(posts.values_list('post_category__category_name', flat=True))
    users_email = User.objects.values_list('email', flat=True)

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Объявления за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=users_email,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
