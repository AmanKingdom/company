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


def get_all_plants_article():
    plant_cates = Category.objects.filter(parent__menu_name='aquatic_plant')
    print('获取水草文章类别', plant_cates)
    if plant_cates:
        plant_articles = []
        for plant_cate in plant_cates:
            temp = plant_cate.articles.all()
            print('获取水草文章', temp)
            if temp:
                for x in temp:
                    plant_articles.append(x)
        return plant_articles
    return None


def homepage(request):
    context = {
        'company': getCompany(),
        'menu1s': getMenu1s(),
        'carousels': Carousel.objects.all().order_by('number'),
        'menu_homepage': True,
        'new_news5': None,
        'case4': None,
        'wechat':getWechat(),
        'plant_articles': get_all_plants_article(),
    }
    context['new_news5'] = Category.objects.get(menu_name='news').articles.order_by('-modified_time')
    if len(context['new_news5']) > 5:
        context['new_news5'] = context['new_news5'][0:5]

    context['case4'] = Category.objects.get(menu_name='case').articles.order_by('-modified_time')
    if len(context['case4']) > 4:
        context['case4'] = context['case4'][0:4]

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
        'current_menu2_brother': None,  # 有current_ment2才有这个，这是给侧边栏的
        'articles': None,
        'article': Article.objects.get(id=id),
        'wechat': getWechat(),
    }
    add_view_number(request, context['article'])
    set_current_menus(context, context['article'].category)

    if context['current_menu2']:    # 有子菜单情况
        context['current_menu2_brother'] = Category.objects.filter(parent_id=context['article'].category.parent_id)
        print(context['article'].category, '的胸弟菜单：', context['current_menu2_brother'])
    else:   # 没有子菜单
        context['articles'] = context['article'].category.articles.order_by('-publish_time')

    return render(request, 'app1/article.html', context=context, status=status.HTTP_200_OK)


def category(request, menu_name):
    print('分类menu_name：', menu_name)
    context = {
        'company': getCompany(),
        'menu1s': getMenu1s(),  # 这里的menu1s是给顶部导航栏的
        'current_menu1': None,
        'current_menu2': None,
        'current_menu2_brother': None,  # 有current_ment2才有这个，这是给侧边栏的
        'articles': None,
        'article': None,
        'wechat': getWechat(),
    }
    cate = Category.objects.get(menu_name=menu_name)
    set_current_menus(context, cate)

    context['articles'] = Article.objects.filter(category_id=cate.id).order_by('-publish_time')

    if context['current_menu2']:    # 有子菜单情况
        context['current_menu2_brother'] = Category.objects.filter(parent_id=cate.parent_id)
        print(cate, '的胸弟菜单：', context['current_menu2_brother'])

    # 不管该菜单的文章是否多篇，都默认展示第一篇的具体内容
    if len(context['articles']) >= 1:
        context['article'] = context['articles'][0]
        if len(context['articles']) == 1:
            context['articles'] = None  # 单篇文章，将无文章列表侧边栏

    if context['article']:  # 不管分类如何，只要是单篇文章都增加阅读量
        add_view_number(request, context['article'])

    return render(request, 'app1/article.html', context=context, status=status.HTTP_200_OK)


def search(request):
    try:
        keyword = request.POST['keyword']
        request.session['keyword'] = keyword
        if keyword == "":
            return HttpResponseRedirect('/')
        elif keyword == "管理系统":
            return HttpResponseRedirect('/manage/')
        else:
            context = {
                'company': getCompany(),
                'articles': [],
                'menu1s': getMenu1s(),
                'menu_homepage': True,
            }

            for art in Article.objects.all():
                if keyword in art.get_pure_content() or keyword in art.title:
                    context['articles'].append(art)

            return render(request, 'app1/search_result.html', context=context)
    except:
        return HttpResponseRedirect('/')
