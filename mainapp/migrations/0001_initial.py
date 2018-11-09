# Generated by Django 2.0.7 on 2018-10-27 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=16, verbose_name='昵称')),
                ('img', models.ImageField(blank=True, null=True, upload_to='upload/%Y/%m/%d/', verbose_name='图片')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='标题')),
                ('authors', models.CharField(max_length=128, verbose_name='作者')),
                ('sore_year', models.IntegerField(verbose_name='发表年度')),
                ('abstract', models.TextField(verbose_name='摘要')),
                ('keywords', models.CharField(blank=True, max_length=128, null=True, verbose_name='关键词')),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='上传时间')),
                ('file', models.FileField(upload_to='upload/%Y/%m/%d/')),
                ('creater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.MyUser', verbose_name='创建者')),
            ],
            options={
                'verbose_name': '文献',
                'verbose_name_plural': '文献',
                'ordering': ['-upload_date'],
                'get_latest_by': 'upload_date',
            },
        ),
        migrations.CreateModel(
            name='Sort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
            ],
            options={
                'verbose_name': '分组',
                'verbose_name_plural': '分组',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='名称')),
                ('source_type', models.CharField(max_length=16, verbose_name='类型')),
                ('img', models.ImageField(blank=True, null=True, upload_to='upload/%Y/%m/%d/', verbose_name='图片')),
            ],
            options={
                'verbose_name': '来源',
                'verbose_name_plural': '来源',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('hash_id', models.CharField(max_length=64, verbose_name='群号')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('creater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.MyUser', verbose_name='创建者')),
                ('managers', models.ManyToManyField(related_name='managers', to='mainapp.MyUser', verbose_name='管理员')),
                ('members', models.ManyToManyField(related_name='members', to='mainapp.MyUser', verbose_name='成员')),
                ('notes', models.ManyToManyField(to='mainapp.Note', verbose_name='文献')),
            ],
            options={
                'verbose_name': '群组',
                'verbose_name_plural': '群组',
            },
        ),
        migrations.AddField(
            model_name='note',
            name='sorts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Sort', verbose_name='分组'),
        ),
        migrations.AddField(
            model_name='note',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Source', verbose_name='来源'),
        ),
    ]
