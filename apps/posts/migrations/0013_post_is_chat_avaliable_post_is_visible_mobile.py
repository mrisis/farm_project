# Generated by Django 4.2 on 2025-02-07 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_post_price_post_unit_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_chat_avaliable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='is_visible_mobile',
            field=models.BooleanField(default=False),
        ),
    ]
