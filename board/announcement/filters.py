import django_filters
from django import forms
from .models import Comment, Post
from urllib import request

# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class ComsFilter(django_filters.FilterSet):
   class Meta:
       model = Comment
       fields = {
           'post': ['in'],
       }
