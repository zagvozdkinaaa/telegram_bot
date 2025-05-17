from django.db import models

# Create your models here.

class UserData(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='id')
    first_name = models.CharField(max_length=100, verbose_name='First name')
    last_name = models.CharField(max_length=100, verbose_name='Last name')
    username = models.CharField(max_length=100, verbose_name='Username')

    class Meta:
        verbose_name='User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id}, {self.username}'