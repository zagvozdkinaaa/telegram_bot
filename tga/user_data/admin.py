from django.contrib import admin
from .models import UserData, News

# Register your models here.

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display=('chat_id', 'username')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display=('title', 'content', 'published_at')