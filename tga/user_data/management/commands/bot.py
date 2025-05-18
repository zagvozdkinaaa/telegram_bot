from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from user_data.models import UserData, News
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
    try:
        latest_news=News.objects.latest('published_at')
        text=f'📰 {latest_news.title}\n\n{latest_news.content}'
    except News.DoesNotExist:
        text='Пока новостей нет.'
        
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

class Command(BaseCommand):
    help = 'Запуск Telegram-бота'

    def handle(self, *args, **options):
        app = Application.builder().token(TOKEN).build()

        app.add_handler(CommandHandler('start', start))
        app.add_handler(CommandHandler('news', news))

        app.run_polling()