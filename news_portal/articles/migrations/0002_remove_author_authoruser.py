# Generated by Django 3.2.5 on 2021-07-09 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='authorUser',
        ),
    ]