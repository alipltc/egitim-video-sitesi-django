# Generated by Django 3.0.6 on 2022-03-24 10:24

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_galeri'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='detail',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
