from django.db import models
from django.utils.text import slugify
from pydantic import ValidationError

from core.models import BaseModel
from apps.accounts.models import User
from apps.files.models import Asset
from apps.locations.models import Province, City
from django.utils.timezone import now
from django.core.exceptions import ValidationError


class PostCategory(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    icon = models.FileField(upload_to='post_category_icons/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subcategories')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.pk:
            original = PostCategory.objects.get(pk=self.pk)
            if original.parent is None and self.parent is not None:
                raise ValidationError({
                    'parent': 'Cannot change parent for a top-level category.'
                })

class Post(BaseModel):
    class UnitPriceChoices(models.TextChoices):
        TOMAN = 'Toman', 'IRT'
        RIAL = 'Rial', 'IRR'

    class PostStatus(models.TextChoices):
        NEW = 'New', 'پست جدید'
        PENDING = 'Pending', 'در حال بررسی'
        APPROVED = 'Approved', 'تایید شده'
        REJECTED = 'Rejected', 'رد شده'

    class RejectionReasonChoices(models.TextChoices):
        DUPLICATE = 'Duplicate', 'تکراری'
        INAPPROPRIATE = 'Inappropriate', 'غیر قابل قبول'
        OTHER = 'Other', 'دیگر'

    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='posts')
    unit_price = models.CharField(max_length=10, choices=UnitPriceChoices.choices, default=UnitPriceChoices.TOMAN,
                                  null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_visible_mobile = models.BooleanField(default=False)
    is_chat_avaliable = models.BooleanField(default=False)

    status = models.CharField(max_length=20, choices=PostStatus.choices, default=PostStatus.NEW)
    rejection_reason = models.CharField(max_length=20, choices=RejectionReasonChoices.choices, null=True, blank=True)
    rejection_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_total_seconds(self):
        return int((now() - self.created_at).total_seconds())

    def clean(self):

        super().clean()
        if self.status == self.PostStatus.REJECTED and not self.rejection_reason:
            raise ValidationError({
                'rejection_reason': 'Rejection reason is required when the post is rejected.'
            })



class PostImage(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='post_images')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Image for by ID {self.asset_id} '


class PostAddress(BaseModel):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='address', null=True, blank=True)
    lat = models.DecimalField(max_digits=10, decimal_places=10, null=True, blank=True)
    lng = models.DecimalField(max_digits=10, decimal_places=10, null=True, blank=True)
    full_address = models.TextField(null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='post_addresses')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='post_addresses')

    def __str__(self):
        return f'Address for {self.post.title} by ID {self.post.id}'


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
        choices=[(i, i) for i in range(6)])

    def __str__(self):
        return f"{self.score} stars by {self.author} for {self.post.id}"

    class Meta:
        unique_together = ['post', 'author']


class FavoritePost(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorited_by')

    def __str__(self):
        return f"User {self.user} favorited Post {self.post}"

    class Meta:
        unique_together = ['post', 'user']
        ordering = ['-created_at']
