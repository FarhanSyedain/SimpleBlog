# Generated by Django 3.0.6 on 2020-09-02 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configrations', '0008_profile_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='thumbnail',
            field=models.ImageField(upload_to='Blog_Thumbnails'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='users'),
        ),
    ]
