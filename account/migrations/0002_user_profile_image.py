# Generated by Django 4.2.7 on 2023-11-22 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='user/images/%Y/%m/%d/'),
        ),
    ]
