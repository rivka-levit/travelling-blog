# Generated by Django 4.2.2 on 2023-06-28 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_author_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='time_read',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]