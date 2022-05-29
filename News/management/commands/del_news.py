from django.core.management.base import BaseCommand, CommandError
from News.models import Post, Category
 

class Command(BaseCommand):
    help = 'Подсказка вашей команды'
 
    def add_arguments(self, parser):
        parser.add_argument('category', type=str)
 
    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')
 
        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
 
        try:
            category = Category.objects.get(article_text=options['category'])
            Post.objects.filter(postCategories=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.article_text}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {category.article_text}'))