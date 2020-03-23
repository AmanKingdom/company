from django.db import models

from DjangoUeditor3.DjangoUeditor.models import UEditorField

import re


class Company(models.Model):
    name = models.CharField('公司名称', max_length=50)
    slogan = models.CharField('口号', max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to='images', null=True, blank=True, verbose_name='logo')
    big_img = models.ImageField(upload_to='images', null=True, blank=True, verbose_name='首页大背景图片')
    dec = UEditorField('公司简介', null=True, blank=True, width=1000, height=300, toolbars="besttome")
    email = models.EmailField('公司邮箱', null=True, blank=True)
    telephone = models.CharField('联系电话', max_length=20, null=True, blank=True)
    phone = models.CharField('手机', max_length=16, null=True, blank=True)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('最新修改时间', auto_now=True)

    def __str__(self):
        return self.name


# 微信公众号
class Wechat(models.Model):
    name = models.CharField('微信公众号名称', max_length=20)
    qrcode = models.ImageField('公众号二维码', upload_to='images')
    logo = models.ImageField('公众号头像', upload_to='images')

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('最新修改时间', auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('分类名称', max_length=20)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='父分类', related_name='child')

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('最新修改时间', auto_now=True)

    def __str__(self):
        return self.name

    def has_children(self):
        children = Category.objects.filter(parent_id=self.id)
        if children:
            return children
        return False


class Article(models.Model):
    title = models.CharField('标题', max_length=100)
    content = UEditorField('内容', width=1000, height=500, toolbars="besttome")
    cover_img = models.ImageField('封面图片', upload_to='images/article_cover_img')
    publish_time = models.DateTimeField('第一次发布时间', auto_now_add=True)
    modified_time = models.DateTimeField('最新修改时间', auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name='文章分类')
    view_number = models.PositiveIntegerField('阅读量', default=0)

    def get_pure_content(self):
        return re.compile(r'<[^>]+>', re.S).sub('', self.content)

    def __str__(self):
        return self.title


# 轮播图
class Carousel(models.Model):
    img = models.ImageField('轮播图图片', upload_to='images/carousel_img')
    title = models.CharField('轮播图标题', max_length=100)
    article = models.ForeignKey(Article, verbose_name='轮播图对应文章id', null=True, blank=True, on_delete=models.CASCADE, related_name='carousels')
    number = models.IntegerField('轮播图序号', default=0)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('最新修改时间', auto_now=True)

    def __str__(self):
        return self.title


# 首页摘要简介
class AbstractText(models.Model):
    title = models.CharField('摘要标题', max_length=100)
    title2 = models.CharField('副标题', max_length=100, null=True, blank=True)
    content = models.TextField('摘要内容')

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('最新修改时间', auto_now=True)

    def __str__(self):
        return self.title


class ViewNumber(models.Model):
    ip = models.CharField('客户端ip', max_length=20)
    article = models.ForeignKey(Article, verbose_name='浏览的文章', on_delete=models.CASCADE)
    number = models.PositiveIntegerField('该客户端浏览此文章的次数', default=1)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('最新修改时间', auto_now=True)

    def __str__(self):
        return self.ip


class Module(models.Model):
    name = models.CharField('模块名称', max_length=50)
    category = models.ForeignKey(Category, verbose_name='对应菜单', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
