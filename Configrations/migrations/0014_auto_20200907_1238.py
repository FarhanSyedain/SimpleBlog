# Generated by Django 3.0.6 on 2020-09-07 17:38

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Configrations', '0013_delete_commentreply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
