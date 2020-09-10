# Generated by Django 3.0.6 on 2020-08-29 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configrations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_page',
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='users'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]