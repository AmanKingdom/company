from django.contrib import admin
from django.contrib.admin import ModelAdmin

from app1.models import AbstractText


@admin.register(AbstractText)
class AbstractTextAdmin(ModelAdmin):
    list_display = ('id', 'title', 'title2', 'create_time', 'modified_time')  # 设置展示的列
    list_editable = ['title', 'title2']
    # search_fields = ('name', )  # 设置可对xx列进行搜索
    # list_filter = ('name', )  # 设置可筛选
    # fields = ('name', ) # 设置详情信息页面所能显示的字段及其顺序
