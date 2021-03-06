# Generated by Django 3.0.5 on 2020-06-05 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='doi_link',
        ),
        migrations.AddField(
            model_name='article',
            name='doi',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='articleauthor',
            unique_together={('author', 'article')},
        ),
    ]
