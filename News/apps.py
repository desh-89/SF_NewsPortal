from django.apps import AppConfig
import redis


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'News'

    def ready(self):
        import News.signals


class PostConfig(AppConfig):
    name = 'News1'
    def ready(self):
        import News.signals

red = redis.Redis(
    host ='redis-10094.c296.ap-southeast-2-1.ec2.cloud.redislabs.com',
    port = 10094,
    password='Mvd5hnt5RHZ1YDif1KbkGOJfiL6GIC13'
)