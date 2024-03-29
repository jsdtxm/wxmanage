# Generated by Django 2.0.7 on 2018-11-06 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0010_auto_20181101_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_priv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes_count', models.IntegerField(blank=True, default=0, null=True, verbose_name='文献数量')),
                ('notes', models.ManyToManyField(blank=True, null=True, to='mainapp.Note', verbose_name='文献')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
    ]
