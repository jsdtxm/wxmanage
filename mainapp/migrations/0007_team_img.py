# Generated by Django 2.0.7 on 2018-11-01 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20181031_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='upload/%Y/%m/%d/', verbose_name='图片'),
        ),
    ]
