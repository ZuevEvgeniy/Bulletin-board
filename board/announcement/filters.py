import django_filters
from django import forms

from .models import Comment

# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class ComsFilter(django_filters.FilterSet):
   date=django_filters.DateFilter(field_name="time_in", widget=forms.DateInput(attrs={'type':"date"}),
                   label='Дата',lookup_expr='date__gte')
   class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Comment
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           #'head_name': ['icontains'],
           'post': ['in'],
                      #'rate': [
               #'lt',  # цена должна быть меньше или равна указанной
               #'gt',  # цена должна быть больше или равна указанной
           #],
       }