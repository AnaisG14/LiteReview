# Generated by Django 4.0 on 2022-01-13 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='review_ok',
        ),
        migrations.AddField(
            model_name='ticket',
            name='number_reviews',
            field=models.IntegerField(default=0),
        ),
    ]
