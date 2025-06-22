# user_data/management/commands/run_bot.py

import os
import sys
import django
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.client.default import DefaultBotProperties


from django.core.management.base import BaseCommand

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tga.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

django.setup()
load_dotenv()

from user_data.models import UserData, News, SentNews

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(Command("start"))
async def start_cmd(message: Message):
    user = message.from_user

    UserData.objects.get_or_create(
        chat_id=user.id,
        defaults={'username': user.username}
    )

    await message.answer("Привет! Я бот спортивных новостей 🏀")


@dp.message(Command("news"))
async def news_cmd(message: Message):
    user = message.from_user

    user_obj, _ = UserData.objects.get_or_create(
        chat_id=user.id,
        defaults={'username': user.username}
    )

    sent_news_ids = SentNews.objects.filter(user=user_obj).values_list('news_id', flat=True)
    next_news = News.objects.exclude(id__in=sent_news_ids).order_by('published_at').first()

    if next_news:
        text = f'📰 <b>{next_news.title}</b>\n\n{next_news.content}'
        await message.answer(text)
        SentNews.objects.create(user=user_obj, news=next_news)
    else:
        await message.answer("У тебя пока нет новых новостей.")


class Command(BaseCommand):
    help = 'Запуск Telegram-бота'

    def handle(self, *args, **options):
        import asyncio
        asyncio.run(dp.start_polling(bot))
