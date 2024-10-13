from django.db import models
from protect.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    text = RichTextUploadingField()
    create_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.header.capitalize()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    comm_text = models.TextField(default=False)
    COMMENT_STATUS = [('pending', 'на рассмотрении'), ('accepted', 'принят'),
                      ('rejected', 'отклонен')]
    status = models.CharField(max_length=10, choices=COMMENT_STATUS, default='pending')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.comm_text) > 124:
            return self.comm_text[:51] + '...'
        else:
            return self.comm_text

    def __str__(self):
        return f'{self.create_time}: {self.comm_text}: {self.user}: {self.status}'
