# Generated by Django 3.1 on 2020-08-23 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camroid_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_img',
            field=models.ImageField(default='ProfileImg/default-avatar.png', upload_to='ProfileImg'),
        ),
    ]
