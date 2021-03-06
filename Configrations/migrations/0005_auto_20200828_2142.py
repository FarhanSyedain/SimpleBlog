# Generated by Django 3.0.6 on 2020-08-29 05:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Configrations', '0004_auto_20200828_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='stars',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(blank=True, to='Configrations.Tag'),
        ),
    ]
