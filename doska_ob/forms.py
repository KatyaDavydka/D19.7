from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Comment
from datetime import date


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {'header', 'text', 'category', 'user'}

    def clean_text(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        if text is not None and len(text) < 20:
            raise ValidationError({
                'text': "Текст не может быть менее 20 символов."
            })

        return text


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {'comm_text'}
