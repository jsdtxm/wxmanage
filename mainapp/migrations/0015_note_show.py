# Generated by Django 2.0.7 on 2018-11-09 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_auto_20181106_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='show',
            field=models.BooleanField(default=True),
        ),
    ]
