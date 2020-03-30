from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework import status

from app1.models import *


def getCompany():
    companys = Company.objects.all()
    if companys:
        return companys[0]
    return None


def getMenu1s():
    menu1s = []
    for menu in Category.objects.all():
        if not menu.parent:
            menu1s.append(menu)
    print('一级菜单分类：', menu1s)
    return menu1s


def getWechat():
    wechats = Wechat.objects.all()
    if wechats:
        return wechats[0]
    return None


def add_view_number(request, art):
    ip = request.META.get('HTTP_X_FORWARDER_FOR', None)
    if not ip:
        ip = request.META.get('REMOTE_ADDR', "")

    view = ViewNumber.objects.filter(ip=str(ip), article=art)
    if view:
        view = view[0]
        if view.modified_time.date() != datetime.today().date():  # 一个用户在同一天内的浏览只当做一个阅读量
            view.number = view.number + 1
            view.save()

            art.view_number = art.view_number + 1
            art.save()
    else:
        ViewNumber.objects.create(ip=str(ip), article=art)

        art.view_number = art.view_number + 1
        art.save()


def homepage(request):
    context = {
        'company': getCompany(),
        'menu1s': getMenu1s(),
        'abstract_texts': AbstractText.objects.all(),
        'wechat': getWechat(),
        'carousels': Carousel.objects.all().order_by('number'),
        'module1': Module.objects.filter(name='首页模块一'),
        'module2': Module.objects.filter(name='首页模块二'),
        'module1_left_articles': None,
        'module1_right_articles': None,
        'module2_left_articles': None,
        'module2_right_articles': None,
    }

    def set_module_and_articles(context, module_name):
        if context[module_name]:
            context[module_name] = context[module_name][0]

            articles = []
            module_categorys = context[module_name].category.has_children()
            if module_categorys:
                for category_item in module_categorys:
                    temp_articles = category_item.articles.all()
                    if temp_articles:
                        articles.extend(temp_articles)
            else:
                articles = context[module_name].category.articles.all()
            if articles:
                articles.sort(key=lambda x: x.modified_time, reverse=True)
                center = int(len(articles)/2)
                if center == 0:
                    center = 1
                context[module_name + '_left_articles'] = articles[:center]
                context[module_name + '_right_articles'] = articles[center:]

    set_module_and_articles(context, 'module1')
    set_module_and_articles(context, 'module2')

    return render(request, 'app1/index.html', context=context, status=status.HTTP_200_OK)


def set_current_menus(context, current_menu):
    if current_menu.parent:
        context['current_menu2'] = current_menu
        context['current_menu1'] = current_menu.parent
    else:
        context['current_menu1'] = current_menu


def article(request, id):
    print('文章id：', id)
    context = {
        'company': getCompany(),
        'menu1s': getMenu1s(),
        'current_menu1': None,
        'current_menu2': None,
        'article': Article.objects.get(id=id)
    }
    add_view_number(request, context['article'])
    set_current_menus(context, context['article'].category)

    return render(request, 'app1/article.html', context=context, status=status.HTTP_200_OK)


def category(request, id):
    print('分类id：', id)
    context = {
        'company': getCompany(),
        'menu1s': getMenu1s(),
        'current_menu1': None,
        'current_menu2': None,
        'articles': None,
        'article': None
    }
    set_current_menus(context, Category.objects.get(id=id))

    context['articles'] = Article.objects.filter(category_id=id).order_by('modified_time')
    if len(context['articles']) == 1:
        context['article'] = context['articles'][0]
        add_view_number(request, context['article'])

    return render(request, 'app1/article.html', context=context, status=status.HTTP_200_OK)


def search(request):
    try:
        keyword = request.POST['keyword']
        if keyword is "":
            return HttpResponseRedirect('/')
        else:
            request.session['keyword'] = keyword
            context = {
                'company': getCompany(),
                'articles': [],
            }

            for art in Article.objects.all():
                if keyword in art.get_pure_content() or keyword in art.title:
                    context['articles'].append(art)

            return render(request, 'app1/search_result.html', context=context)
    except:
        return HttpResponseRedirect('/')
