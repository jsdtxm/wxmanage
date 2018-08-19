from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class MyUser(models.Model):
    #用户
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField('昵称',max_length=16)
    img = models.ImageField(verbose_name='图片',upload_to='upload/%Y/%m/%d/',null=True,blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

class Source(models.Model):
    #来源
    name = models.CharField('名称', max_length=32)
    source_type = models.CharField('类型', max_length=16)
    img = models.ImageField(verbose_name='图片',upload_to='upload/%Y/%m/%d/',null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "来源"
        verbose_name_plural = verbose_name

class Sort(models.Model):
    #分组
    name = models.CharField('名称', max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "分组"
        verbose_name_plural = verbose_name

class Note(models.Model):
    '''文献'''
    title = models.CharField('标题', max_length=64)
    authors = models.CharField('作者', max_length=128)
    source =  models.ForeignKey(Source,verbose_name='来源',on_delete=models.CASCADE)
    sore_year = models.IntegerField('发表年度')
    abstract = models.TextField('摘要')
    keywords = models.CharField('关键词',max_length=128)
    #上传时间
    upload_date = models.DateTimeField('上传时间', default=now)
    #文件
    file = models.FileField(upload_to='upload/%Y/%m/%d/')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-upload_date']
        verbose_name = "文献"
        verbose_name_plural = verbose_name
        get_latest_by = 'upload_date'

class Note_middle(models.Model):
    '''文献_中介'''
    sorts = models.ForeignKey(Sort,verbose_name='分组',on_delete=models.CASCADE)
    notes = models.ForeignKey(Note, verbose_name='文献',on_delete=models.CASCADE)
    upload_date = models.DateTimeField('上传时间', default=now)
    creater = models.ForeignKey(MyUser, verbose_name='创建者', on_delete=models.CASCADE)

    def __str__(self):
        return self.notes.title

    class Meta:
        ordering = ['-upload_date']
        verbose_name = "文献_中介"
        verbose_name_plural = verbose_name
        get_latest_by = 'upload_date'


class Team(models.Model):
    #群组
    name = models.CharField('名称',max_length=16)
    hash_id = models.CharField('群号',max_length=64)
    created_time = models.DateTimeField('创建时间', default=now)
    creater = models.ForeignKey(MyUser, verbose_name='创建者', on_delete=models.CASCADE)
    managers = models.ManyToManyField(MyUser, verbose_name='管理员',related_name='managers')
    members = models.ManyToManyField(MyUser, verbose_name='成员',related_name='members')
    notes = models.ManyToManyField(Note_middle, verbose_name='文献')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "群组"
        verbose_name_plural = verbose_name
