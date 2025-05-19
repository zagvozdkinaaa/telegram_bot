from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from user_data.models import UserData, News, SentNews
import os
import sys
import django
from dotenv import load_dotenv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tga.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
load_dotenv()
TOKEN = os.getenv('TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user=update.effective_user
    UserData.objects.get_or_create(
        chat_id=user.id,
        defaults={'username': user.username}
    )
    await update.message.reply_text('Привет! Я бот спортивных новостей 🏀')

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    user_obj, _ = UserData.objects.get_or_create(
        chat_id=user.id,
        defaults={'username': user.username}
    )

    sent_news_ids = SentNews.objects.filter(user=user_obj).values_list('news_id', flat=True)
    next_news = News.objects.exclude(id__in=sent_news_ids).order_by('published_at').first()

    if next_news:
        text = f'📰 {next_news.title}\n\n{next_news.content}'
        await context.bot.send_message(chat_id=user.id, text=text)
        SentNews.objects.create(user=user_obj, news=next_news)
    else:
        await context.bot.send_message(chat_id=user.id, text="У тебя пока нет новых новостей.")

class Command(BaseCommand):
    help = 'Запуск Telegram-бота'

    def handle(self, *args, **options):
        app = Application.builder().token(TOKEN).build()

        app.add_handler(CommandHandler('start', start))
        app.add_handler(CommandHandler('news', news))

        app.run_polling()