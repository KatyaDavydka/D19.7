from django import forms
from django.contrib import admin
from .models import *

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostsAdmin(admin.ModelAdmin):
    list_display = ('header', 'text', 'create_time')
    list_filter = ('user__username', 'create_time')
    form = PostAdminForm


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
