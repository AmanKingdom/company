import json

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.shortcuts import render
from django.views import View
from rest_framework import status

from app1.models import Company, Wechat, Category, Article, Carousel
from app1.views import getCompany, getWechat, getMenu1s, set_current_menus
from app_manage.forms import LoginForm, CompanyImageForm, WechatImageForm, ContentForm, ArticleImageForm, \
    CarouselImageForm
from app_manage.models import User

CATEGORYS = [
    {'name': '新闻动态', 'menu_name': 'news', 'parent': None},
    {'name': '公司简介', 'menu_name': 'introduction', 'parent': None},

    {'name': '业务介绍', 'menu_name': 'business', 'parent': None},
    {'name': '水生态修复', 'menu_name': 'water_ecological_restoration', 'parent': 'business'},
    {'name': '臭黑水治理', 'menu_name': 'black_water_treatment', 'parent': 'business'},
    {'name': '栖息地修复', 'menu_name': 'habitat_restoration', 'parent': 'business'},
    {'name': '河湖生态运营维护', 'menu_name': 'water_ecological_maintenance', 'parent': 'business'},
    {'name': '自然教育', 'menu_name': 'natural_ducation', 'parent': 'business'},

    {'name': '水生植物', 'menu_name': 'aquatic_plant', 'parent': None},
    {'name': '沉水植物', 'menu_name': 'submerged_plant', 'parent': 'aquatic_plant'},
    {'name': '浮叶植物', 'menu_name': 'floating_leaf_plant', 'parent': 'aquatic_plant'},
    {'name': '挺水植物', 'menu_name': 'emergent_plant', 'parent': 'aquatic_plant'},
    {'name': '湿生植物', 'menu_name': 'hygrophyte', 'parent': 'aquatic_plant'},

    {'name': '生产基地', 'menu_name': 'production_base', 'parent': None},
    {'name': '广东东莞基地', 'menu_name': 'dongguan', 'parent': 'production_base'},
    {'name': '广西南宁基地', 'menu_name': 'nanning', 'parent': 'production_base'},

    {'name': '工程案例', 'menu_name': 'case', 'parent': None},
    {'name': '联系我们', 'menu_name': 'contact_us', 'parent': None},
]


def init_menu(request):
    """
    初始化文章分类（即首页菜单)
    :param request:
    :return:就返回个json格式数据OK了，仅限我使用，别人不需要使用
    """
    categorys = Category.objects.all()
    if categorys:
        print('已经有文章分类')
    else:
        print('还没有文章分类了，创建')
        for cate in CATEGORYS:
            if cate['parent']:
                parent = Category.objects.get(menu_name=cate['parent'])
                cate['parent_id'] = parent.id
            del cate['parent']
            Category.objects.create(**cate)
    return JsonResponse({'status': True})


def set_menus(name):
    menus = {
        'homepage': {
            'active': False,
            'url_name': 'homepage',
            'name': '官网首页'
        },
        'manage_company': {
            'active': False,
            'url_name': 'manage_company',
            'name': '公司信息'
        },
        'manage_wechat': {
            'active': False,
            'url_name': 'manage_wechat',
            'name': '微信公众号'
        },
        'manage_articles': {
            'active': False,
            'url_name': 'manage_articles',
            'name': '文章管理'
        },
        'manage_carousels':{
            'active': False,
            'url_name': 'manage_carousels',
            'name': '轮播图管理'
        },
        'write_article': {
            'active': False,
            'url_name': 'write_article',
            'name': '写文章'
        },
    }
    menus[name]['active'] = True
    return menus


def modifily_data(name_list, data, model, id):
    need_change_data = {}
    for name in name_list:
        value = data.get(name, "")
        print(value, type(value))
        if value != model.objects.get(id=id).__getattribute__(name):
            need_change_data[name] = value

    if need_change_data:
        print('将修改数据为：', need_change_data)
        model.objects.filter(id=id).update(**need_change_data)


@login_required(login_url='/manage/login')
def manage_company(request):
    context = {
        'company': getCompany(),
        'company_image_form': CompanyImageForm(instance=getCompany()),
        'menus': set_menus('manage_company')
    }

    if request.method == 'GET':
        return render(request, 'app_manage/company.html', context=context)
    elif request.method == 'POST':  # 因为前端是用form表单，form表单只能用post和get，所以就用post替代put来修改数据好了
        # put_data = json.loads(list(request.POST.keys())[0])   # 用表单提交的数据直接就是字典形式，不需要转换
        put_data = request.POST
        print('接收到post修改的公司信息：', put_data)

        print('查看请求头', request.headers)

        # 先检查更新logo图片的数据
        company_image_form = CompanyImageForm(request.POST, request.FILES, instance=context['company'])
        if company_image_form.is_valid():
            company_image_form.save()

        # 后更新其余数据
        name_list = ['name', 'slogan', 'email', 'telephone', 'phone', 'qq', 'wechat', 'address', 'icp']
        modifily_data(name_list, put_data, Company, context['company'].id)

        return HttpResponseRedirect('/manage')
    else:
        print('???not get and not post? what are you doing?')
        return HttpResponseRedirect('/')


@login_required(login_url='/')
def manage_wechat(request):
    context = {
        'menus': set_menus('manage_wechat'),
        'wechat': getWechat(),
        'wechat_image_form': WechatImageForm(instance=getWechat()),
    }

    if request.method == 'GET':
        return render(request, 'app_manage/wechat.html', context=context)
    elif request.method == 'POST':  # 因为前端是用form表单，form表单只能用post和get，所以就用post替代put来修改数据好了
        put_data = request.POST
        print('接收到post修改的微信公众号信息：', put_data)

        # 先更新两张图片的数据
        wechat_image_form = WechatImageForm(request.POST, request.FILES, instance=context['wechat'])
        if wechat_image_form.is_valid():
            wechat_image_form.save()

        # 后更新其余数据
        name_list = ['name', ]
        modifily_data(name_list, put_data, Wechat, context['wechat'].id)

        return HttpResponseRedirect('/manage/manage_wechat')
    else:
        print('???not get and not post? what are you doing?')
        return HttpResponseRedirect('/')


@login_required(login_url='/')
def manage_articles(request):
    context = {
        'menus': set_menus('manage_articles'),
        'menu1s': getMenu1s(),
        'current_menu1': None,
        'current_menu2': None,
        'articles': None,
    }

    if request.method == 'GET':
        if context['menu1s']:
            if context['menu1s'][0].has_children():
                set_current_menus(context, context['menu1s'][0].has_children()[0])
            else:
                set_current_menus(context, context['menu1s'][0])
            if context['current_menu2']:
                context['articles'] = Article.objects.filter(category=context['current_menu2'])
            else:
                context['articles'] = Article.objects.filter(category=context['current_menu1'])
        return render(request, 'app_manage/articles.html', context=context)

    else:
        print('???not get and not post? what are you doing?')
        return HttpResponseRedirect('/')


def carousel_up(id):
    up_carousel = Carousel.objects.get(id=id)
    number = int(up_carousel.number)
    if number > 1:
        # 和要上移对象的上一个对象交换序号
        Carousel.objects.filter(number=(number - 1)).update(number=number)
        Carousel.objects.filter(id=id).update(number=(number - 1))


def carousel_down(id):
    down_carousel = Carousel.objects.get(id=id)
    number = int(down_carousel.number)

    if 1 <= number < len(Carousel.objects.all()):
        Carousel.objects.filter(number=(number + 1)).update(number=number)
        Carousel.objects.filter(id=id).update(number=(number + 1))


@login_required(login_url='/')
def carousel(request):  # 新建轮播图
    if request.method == 'GET':
        context = {
            'carousel_image_form': CarouselImageForm(),
            'menus': set_menus('manage_carousels')
        }
        return render(request, 'app_manage/carousel.html', context=context)
    elif request.method == 'POST':
        post_data = request.POST
        print('接收到post新增的轮播图信息：', post_data)
        carousel_image_form = CarouselImageForm(post_data, request.FILES)

        number = len(Carousel.objects.all()) + 1

        if carousel_image_form.is_valid():
            carousel = carousel_image_form.save()

            # 后更新其余数据
            carousel.number = number
            carousel.title = post_data.get('title')
            carousel.save()

            return HttpResponseRedirect('/manage/manage_carousels')

        return HttpResponseRedirect('/manage/carousel')


@login_required(login_url='/')
def manage_carousels(request):
    if request.method == 'GET':
        context = {
            'carousels': Carousel.objects.all().order_by('number'),
            'menus': set_menus('manage_carousels')
        }
        return render(request, 'app_manage/carousels.html', context=context)
    elif request.method == 'PUT':
        put_data = json.loads(list(QueryDict(request.body).keys())[0])
        print('接收到put修改的轮播图id：', put_data, type(put_data))

        if int(put_data['operate']) == 1:
            carousel_up(put_data['id'])
        elif int(put_data['operate']) == 0:
            carousel_down(put_data['id'])

        return JsonResponse({'message': None})
    elif request.method == 'DELETE':
        try:
            delete_data = json.loads(list(QueryDict(request.body).keys())[0])
            print('将删除的轮播图的id为：', delete_data)
            Carousel.objects.filter(id=delete_data['id']).delete()
            return JsonResponse({'message': None})
        except Exception:
            return JsonResponse({'message': '删除数据失败！请重试'})


def getMenu12s():
    """
    获取没有子菜单的分类菜单
    :return:
    """
    all_menus = Category.objects.all()
    menu12s = []
    for menu in all_menus:
        if not menu.has_children():
            menu12s.append(menu)
    return menu12s


@login_required(login_url='/')
def write_article(request):  # 新建文章
    context = {
        'content_form': ContentForm(),
        'article_image_form': ArticleImageForm(),
        'menus': set_menus('write_article'),
        'menu12s': getMenu12s()
    }

    if request.method == 'GET':
        return render(request, 'app_manage/article.html', context=context)
    if request.method == 'POST':
        post_data = request.POST
        print('接收到post新增的文章数据：', post_data)

        # 先设置封面图片
        article_image_form = ArticleImageForm(request.POST, request.FILES)
        if article_image_form.is_valid():
            article = article_image_form.save()

            # 后更新其余数据
            name_list = ['title', 'content', 'category_id']
            modifily_data(name_list, post_data, Article, article.id)
            return HttpResponseRedirect('/manage/manage_articles')
        else:
            return HttpResponseRedirect('/')


@login_required(login_url='/')
def manage_article(request, id):  # 修改文章
    context = {
        'article': Article.objects.get(id=id),
        'content_form': ContentForm(),
        'article_image_form': ArticleImageForm(instance=Article.objects.get(id=id)),
        'menus': set_menus('write_article'),
        'menu12s': getMenu12s()
    }

    if request.method == 'GET':
        return render(request, 'app_manage/article.html', context=context)
    elif request.method == 'POST':  # 前端是form表单提交，所以以post为put
        put_data = request.POST
        print('接收到post修改的文章数据：', put_data)

        # 先设置封面图片
        article_image_form = ArticleImageForm(request.POST, request.FILES, instance=context['article'])
        if article_image_form.is_valid():
            article_image_form.save()

        # 后更新其余数据
        name_list = ['title', 'content', 'category_id']
        modifily_data(name_list, put_data, Article, id)
        return HttpResponseRedirect('/manage/manage_article/' + id)
    elif request.method == 'DELETE':
        try:
            print('将删除的文章的id为：', id)
            Article.objects.filter(id=id).delete()
            return JsonResponse({'message': None})
        except Exception:
            return JsonResponse({'message': '删除数据失败！请重试'})


@login_required(login_url='/')
def select_category(request, id):
    print('管理端-分类id：', id)
    context = {
        'menus': set_menus('manage_articles'),
        'menu1s': getMenu1s(),
        'current_menu1': None,
        'current_menu2': None,
        'articles': None,
        'carousels': Carousel.objects.all().order_by('number')
    }
    set_current_menus(context, Category.objects.get(id=id))

    context['articles'] = Article.objects.filter(category_id=id).order_by('-modified_time')

    return render(request, 'app_manage/articles.html', context=context)


class LoginView(View):
    def get(self, request):
        return render(request, 'app_manage/login.html')

    def post(self, request):
        context = {
            'message': None,
        }
        login_form = LoginForm(request.POST)
        print('登录信息：', request.POST)
        if login_form.is_valid():
            if User.objects.filter(username=login_form.cleaned_data['username']):
                print('存在此账号')
                user = authenticate(**login_form.cleaned_data)
                if user:
                    print('获取到user')
                    if user.is_active:
                        login(request, user)
                        print(user.username, '登录成功')
                        request.session['username'] = user.username
                        return HttpResponse(json.dumps(context, ensure_ascii=False),
                                            content_type='application/json',
                                            charset='utf-8', status=status.HTTP_200_OK)
                    else:
                        context['message'] = '该用户已被注销'
                else:
                    context['message'] = '密码错误'
            else:
                context['message'] = '此账号不存在'
        else:
            context['message'] = '请填写账号密码'

        return HttpResponse(json.dumps(context, ensure_ascii=False),
                            content_type='application/json',
                            charset='utf-8', status=status.HTTP_401_UNAUTHORIZED)


def logout_view(request):
    print('退出登录')
    logout(request)
    return HttpResponseRedirect('/')
