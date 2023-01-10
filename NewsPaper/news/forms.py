from django import forms
from django.core.exceptions import ValidationError

from .models import Post

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'post_author',
           'categories',
           'title',
           'post_text',
       ]

       def clean(self):
           cleaned_data = super().clean()
           name = cleaned_data.get("title")
           description = cleaned_data.get("post_text")

           if name == description:
               raise ValidationError(
                   "Заголовок не должен быть одинаковым с текстом"
               )

           return cleaned_data