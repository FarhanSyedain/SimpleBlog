# Generated by Django 3.0.6 on 2020-09-01 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configrations', '0007_blogpost_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='history',
            field=models.TextField(blank=True, null=True),
        ),
    ]
