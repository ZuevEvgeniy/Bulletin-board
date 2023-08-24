from django import forms
from .models import Post, Comment
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
            #'author',
            'category',
            'head_name',
            'article_text',
        ]

   def __init__(self, user_info, *args, **kwargs):
       self.user_info = user_info
       super().__init__(*args, **kwargs)

   def clean(self):
       cleaned_data = super().clean()
       cleaned_data['author'] = self.user_info
       article_text = cleaned_data.get("article_text")
       if article_text is not None and len(article_text) < 20:
           raise ValidationError({
               "article_text": "Публикация не может быть менее 20 символов."
           })
       head_name = cleaned_data.get("head_name")
       if head_name == article_text :
           raise ValidationError(
               "Название не должно быть идентично посту."
           )

       return cleaned_data

class ComForm(forms.ModelForm):
   class Meta:
       model = Comment
       fields = [
            #'user',
            'post',
            'comment_text',
        ]
   def __init__(self, user_info, *args, **kwargs):
       self.user_info = user_info
       super().__init__(*args, **kwargs)

   def clean(self):
       cleaned_data = super().clean()
       cleaned_data['user'] = self.user_info
       comment_text = cleaned_data.get("comment_text")
       if comment_text is not None and len(comment_text) < 5:
           raise ValidationError({
               "comment_text": "Публикация не может быть менее 5 символов."
           })

       return cleaned_data
