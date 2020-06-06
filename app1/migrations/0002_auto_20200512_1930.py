# Generated by Django 2.2 on 2020-05-12 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carousel',
            name='article',
        ),
        migrations.AlterField(
            model_name='carousel',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='轮播图标题'),
        ),
    ]