# Generated by Django 3.0.6 on 2022-03-31 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcart',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]