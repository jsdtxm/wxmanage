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
    name = models.CharField('名称', max_length=256)
    source_type = models.CharField('类型', max_length=16)
    img = models.ImageField(verbose_name='图片',upload_to='upload/%Y/%m/%d/',null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "来源"
        verbose_name_plural = verbose_name

class Sort(models.Model):
    #分组
    name = models.CharField('名称', max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "分组"
        verbose_name_plural = verbose_name

class QNote(models.Model):
    '''引用文献'''
    title = models.CharField('标题', max_length=256)
    authors = models.CharField('作者', max_length=128)
    institution = models.CharField('机构', max_length=128)
    quoted = models.IntegerField('被引量')
    sore_year = models.IntegerField('发表年度')
    url = models.CharField('链接', max_length=512)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = "引用文献"
        verbose_name_plural = verbose_name
        get_latest_by = 'title'

class Note(models.Model):
    '''文献'''
    title = models.CharField('标题', max_length=256)
    authors = models.CharField('作者', max_length=128)
    source =  models.ForeignKey(Source,verbose_name='来源',on_delete=models.CASCADE,null=True,blank=True)
    doi = models.CharField('数字对象唯一标识符', max_length=128)
    institution = models.CharField('机构', max_length=128)
    sore_year = models.IntegerField('发表年度')
    abstract = models.TextField('摘要')
    sorts = models.ForeignKey(Sort,verbose_name='分组',on_delete=models.CASCADE,null=True,blank=True)
    keywords = models.CharField('关键词',max_length=128,null=True,blank=True)
    creater = models.ForeignKey(MyUser, verbose_name='创建者', on_delete=models.CASCADE,null=True,blank=True)
    upload_date = models.DateTimeField('上传时间', default=now)
    quotes = models.ManyToManyField(QNote, verbose_name='参考文献',related_name='quotes',null=True,blank=True)
    show = models.BooleanField('是否显示',default=True)
    #文件
    upfile = models.FileField(upload_to='upload/%Y/%m/%d/',null=True,blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-upload_date']
        verbose_name = "文献"
        verbose_name_plural = verbose_name
        get_latest_by = 'upload_date'

class User_priv(models.Model):
    #用户私有文献组
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    notes = models.ManyToManyField(Note, verbose_name='文献',null=True,blank=True)
    notes_count = models.IntegerField('文献数量', default=0,null=True,blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "用户私有文献组"
        verbose_name_plural = verbose_name

class Team(models.Model):
    #群组
    name = models.CharField('名称',max_length=64)
    hash_id = models.CharField('群号',max_length=64)
    introduce = models.TextField('介绍',max_length=1024)
    created_time = models.DateTimeField('创建时间', default=now)
    creater = models.ForeignKey(MyUser, verbose_name='创建者', on_delete=models.CASCADE)
    managers = models.ManyToManyField(MyUser, verbose_name='管理员',related_name='managers')
    members = models.ManyToManyField(MyUser, verbose_name='成员',related_name='members')
    member_count = models.IntegerField('成员数量', default=1,null=True,blank=True)
    notes = models.ManyToManyField(Note, verbose_name='文献',null=True,blank=True)
    notes_count = models.IntegerField('文献数量', default=0,null=True,blank=True)
    img = models.ImageField(verbose_name='图片',upload_to='upload/%Y/%m/%d/',null=True,blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "群组"
        verbose_name_plural = verbose_name
