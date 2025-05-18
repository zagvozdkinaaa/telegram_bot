from django.db import models

# Create your models here.

class UserData(models.Model):
    chat_id = models.IntegerField(
        primary_key=True, 
        verbose_name='chat_id'
        )
    username = models.CharField(
        max_length=100, 
        verbose_name='Username'
        )

    class Meta:
        verbose_name='User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.chat_id}, {self.username}'
    
class News(models.Model):
    title=models.CharField(
        max_length=255,
        verbose_name='Title'
    )
    content=models.TextField(
        verbose_name='Content'
    )
    published_at=models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date of publication'
    )

    class Meta:
        verbose_name='News'
        verbose_name_plural='News'

    def __str__(self):
        return f'{self.title}, {self.published_at}'