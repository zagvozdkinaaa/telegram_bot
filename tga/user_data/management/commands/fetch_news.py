from django.core.management.base import BaseCommand
import os
import requests
from dotenv import load_dotenv
from ...models import News

load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def fetch_and_save_news():
    url = f'https://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey={NEWS_API_KEY}'
    response=requests.get(url)
    articles=response.json().get('articles', [])

    for article in articles:
        title=article.get('title')
        content=article.get('description') or 'Без описания'
        if title:
            News.objects.get_or_create(title=title, defaults={'content': content})

class Command(BaseCommand):
    help = 'Загружает свежие новости из API и сохраняет в базу данных'

    def handle(self, *args, **options):
        fetch_and_save_news()
        self.stdout.write(self.style.SUCCESS('Новости успешно загружены!'))