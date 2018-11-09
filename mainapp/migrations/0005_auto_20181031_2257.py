# Generated by Django 2.0.7 on 2018-10-31 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20181031_2256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qnote',
            old_name='quotes',
            new_name='quoted',
        ),
        migrations.AlterField(
            model_name='note',
            name='quotes',
            field=models.ManyToManyField(related_name='quotes', to='mainapp.QNote', verbose_name='参考文献'),
        ),
    ]
