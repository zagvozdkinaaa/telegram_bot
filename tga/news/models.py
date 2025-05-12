from django.db import models

# Create your models here.

class News(models.Model):
    title=models.CharField(
        max_length=255,
        verbose_name='Title'
    )
    content=models.TextField(
        verbose_name='Content'
    )
    category=models.CharField(
        max_length=100,
        verbose_name='Category',
        blank=True
    )
    published_at=models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date of publication'
    )
    source=models.URLField(
        verbose_name='Source',
        blank=True
    )
    def __str__(self):
        return f'{self.title} {self.published_at.date()}'
    
    class Meta:
        verbose_name='News'
        verbose_name_plural='News'