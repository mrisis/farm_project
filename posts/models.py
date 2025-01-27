from django.db import models
from core.models import BaseModel
from django.utils.text import slugify
from accounts.models import User
from files.models import Asset



class PostCategory(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subcategories')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Post(BaseModel):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='posts')

    def __str__(self):
        return f'{self.title} by {self.author}'


class PostImage(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='post_images')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Image for {self.post.title} by ID {self.post.id}'



class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')

    def __str__(self):
        return f'Comment by {self.author} on {self.post.id}'

class Rating(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField(
        choices=[(i , i) for i in range(6) ])


    def __str__(self):
        return f"{self.score} stars by {self.author} for {self.post.id}"

    class Meta:
        unique_together = ['post', 'author']

