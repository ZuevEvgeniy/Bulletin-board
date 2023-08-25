from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.core.cache import cache

tanks = 'Танки'
hils = 'Хилы'
dd = 'ДД'
merchants = 'Торговцы'
guild_masters = 'Гилдмастеры'
quest_givers = 'Квестгиверы'
blacksmiths = 'Кузнецы'
tanners = 'Кожевники'
potion_makers = 'Зельевары'
spell_masters = 'Мастера заклинаний'
class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


CATEGORY = [
    (tanks, 'Танки'),
    (hils, 'Хилы'),
    (dd, 'ДД'),
    (merchants, 'Торговцы'),
    (guild_masters, 'Гилдмастеры'),
    (quest_givers, 'Квестгиверы'),
    (blacksmiths, 'Кузнецы'),
    (tanners, 'Кожевники'),
(potion_makers, 'Зельевары'),
(spell_masters, 'Мастера заклинаний'),
]


class Post(models.Model):

    objects = None
    author = models.ForeignKey(User, on_delete=models.CASCADE, default= "1")
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20,choices=CATEGORY, default=tanks)
    head_name = models.CharField(max_length=250, unique=True)
    article_text = models.TextField()
    image = models.ImageField(upload_to='images/',blank=False, null= True)
    file = models.FileField(upload_to='files/',blank=False, null= True)

    def __str__(self):
        return self.head_name

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его

class Comment(models.Model):

    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE,default="1")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default= "1")
    comment_text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    def get_absolute_url(self):
        return reverse('com_detail', args=[str(self.id)])

    def __str__(self):
        return self.post
