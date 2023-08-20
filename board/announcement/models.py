from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.core.cache import cache

tanks = 'TNK'
hils = 'HIL'
dd = 'DD'
merchants = 'MCH'
guild_masters = 'GMA'
quest_givers = 'QMA'
blacksmiths = 'BLM'
tanners = 'TAN'
potion_makers = 'PMK'
spell_masters = 'SMA'
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

class Comment(models.Model):

    objects = None
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)

    def like(self):
        return self.user #при принятии отклика, вернуть имя, чтоб письмо

    def dislike(self):
        self.delete() #при непринятии отклика, удалить
        self.save()
class Post(models.Model):

    objects = None
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=3, choices=CATEGORY, default=tanks)
    head_name = models.CharField(max_length=250, unique=True)
    article_text = models.TextField()
    comment = models.ManyToManyField(Comment, through="PostComment")

    def __str__(self):
        return self.head_name

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его

class PostComment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
