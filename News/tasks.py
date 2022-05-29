from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from .models import Post, Category
from django.template.loader import render_to_string
from datetime import datetime as date_time

@shared_task
def send_new_mail(username, email, html_content):
    msg = EmailMultiAlternatives(
        subject=f'Здравствуй, {username}. Новая статья в вашем разделе!',
        from_email='testskillfactory@gmail.com',
        to=[email]
    )

    msg.attach_alternative(html_content, 'text/html')

    msg.send()

@shared_task
def send_new_mails_weekly(username, email, html_content):
    for category in Category.objects.all():
        news_from_each_category = []
        week_number_last = date_time.now().isocalendar()[1] - 1
        for news in Post.objects.filter(id=category.id, datetime__week=week_number_last).values('pk',
                                                                                    'title',
                                                                                    'datetime',
                                                                                    'categoryType'):
            date_format = news.get("datetime").strftime("%m/%d/%Y")
            new = (f' http://127.0.0.1:8000/news/{news.get("pk")}, {news.get("title")}, '
                   f'Категория: {news.get("categoryType")}, Дата создания: {date_format}')
            news_from_each_category.append(new)

        subscribers = category.subscribers.all()

        for subscriber in subscribers:
            html_content = render_to_string(
                'mail_sender.html', {'user': subscriber,
                                     'text': news_from_each_category,
                                     'category_name': category.article_text,
                                     'week_number_last': week_number_last})
            msg = EmailMultiAlternatives(
                subject=f'Здравствуй, {subscriber.username}, новые статьи за прошлую неделю в вашем разделе!',
                from_email='testskillfactory@gmail.com',
                to=[subscriber.email]
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()