# Generated by Django 2.0.7 on 2018-11-06 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_auto_20181106_2129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='file',
            new_name='upfile',
        ),
    ]
