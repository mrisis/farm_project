# Generated by Django 4.2 on 2025-02-17 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_asset_title'),
        ('accounts', '0006_userrole'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_profile_image', to='files.asset'),
        ),
    ]
