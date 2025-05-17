from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from user_data.models import UserData
import os
import sys
import django
from dotenv import load_dotenv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
load_dotenv()
TOKEN = os.getenv('TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user=update.effective_user
    UserData.objects.get_or_create(
        id=user.id,
        defaults={'username': user.username}
    )
    await update.message.reply_text('Привет! Я бот спортивных новостей 🏀')

class Command(BaseCommand):
    help = 'Запуск Telegram-бота'

    def handle(self, *args, **options):
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler('Start', start))
        app.run_polling()