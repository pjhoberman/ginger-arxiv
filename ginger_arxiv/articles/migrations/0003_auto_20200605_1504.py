# Generated by Django 3.0.5 on 2020-06-05 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20200605_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='link',
            field=models.URLField(db_index=True, unique=True),
        ),
    ]
