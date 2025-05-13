import os
import sys
import signal
import asyncio
import django
from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from news.models import News
from user_data.models import UserData

PROJECT_ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tga.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

load_dotenv()

class Command(BaseCommand):
    help = "Run telegram bot"
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.application = None
        self.loop = None
        self.shutdown_event = asyncio.Event()

        async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_id=update.effective_user.id