# Generated by Django 3.0.6 on 2022-05-14 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_faq'),
    ]

    operations = [
        migrations.RenameField(
            model_name='faq',
            old_name='siranumber',
            new_name='siranumara',
        ),
        migrations.RemoveField(
            model_name='faq',
            name='ordernumber',
        ),
    ]
