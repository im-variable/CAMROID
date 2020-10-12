# Generated by Django 3.0.7 on 2020-10-12 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camroid_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorylist',
            name='Cat_Img',
            field=models.ImageField(upload_to='cat_media'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_img',
            field=models.ImageField(default='media/ProfileImg/default-avatar.png', upload_to='ProfileImg'),
        ),
    ]
