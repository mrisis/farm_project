# Generated by Django 4.2 on 2025-01-27 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='object_id',
        ),
    ]