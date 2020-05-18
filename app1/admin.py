from django.contrib import admin
from django.contrib.admin import ModelAdmin

from app1.models import *


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    list_display = ('id', 'name', 'email', 'telephone', 'phone', 'create_time', 'modified_time')  # 设置展示的列
    list_editable = ['name', 'email', 'telephone', 'phone']
    # search_fields = ('name', )  # 设置可对xx列进行搜索
    # list_filter = ('name', )  # 设置可筛选
    # fields = ('name', ) # 设置详情信息页面所能显示的字段及其顺序


@admin.register(Wechat)
class WechatAdmin(ModelAdmin):
    list_display = ('id', 'name', 'create_time', 'modified_time')
    list_editable = ['name', ]


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name', 'create_time', 'modified_time')
    list_editable = ['name', ]


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ('id', 'title', 'view_number', 'publish_time', 'modified_time')
    search_fields = ('title', )
    list_editable = ['title', 'view_number']


@admin.register(Carousel)
class CarouselAdmin(ModelAdmin):
    list_display = ('id', 'title', 'number', 'create_time', 'modified_time')
    list_editable = ['title', 'number']


@admin.register(ViewNumber)
class ViewNumberAdmin(ModelAdmin):
    list_display = ('id', 'ip', 'number', 'create_time', 'modified_time')
    list_editable = ['ip', 'number']


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ('id', 'content', 'name', 'phone', 'email', 'address')
    list_editable = ['content', 'name', 'phone', 'email', 'address']