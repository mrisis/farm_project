# Generated by Django 4.2 on 2025-01-29 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rolecategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, help_text='This is deleted datetime', null=True, verbose_name='Deleted Datetime')),
                ('is_deleted', models.BooleanField(db_index=True, default=False, editable=False, help_text='This is deleted status', verbose_name='Deleted status')),
                ('is_active', models.BooleanField(default=True, editable=False, help_text='This is active status', verbose_name='Active status')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='accounts.rolecategory')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
