# Generated by Django 3.2.9 on 2021-11-16 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_category_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='category name', max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='postcategory',
            name='postThrough',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.post', verbose_name='This is the help text'),
        ),
    ]
