import json

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.shortcuts import render
from django.views import View
from rest_framework import status

from app1.models import Company, AbstractText, Wechat, Category, Article, Carousel, Module
from app1.views import getCompany, getWechat, getMenu1s, set_current_menus
from app_manage.forms import LoginForm, DecForm, CompanyImageForm, WechatImageForm, ContentForm, ArticleImageForm
from app_manage.models import User


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
        'manage_abstract_text': {
            'active': False,
            'url_name': 'manage_abstract_text',
            'name': '首页摘要'
        },
        'manage_wechat': {
            'active': False,
            'url_name': 'manage_wechat',
            'name': '微信公众号'
        },
        # 'manage_carousel': {
        #     'active': False,
        #     'url_name': 'manage_carousel',
        #     'name': '首页轮播图'
        # },
        'manage_category': {
            'active': False,
            'url_name': 'manage_category',
            'name': '菜单分类'
        },
        'manage_articles': {
            'active': False,
            'url_name': 'manage_articles',
            'name': '文章管理'
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


@login_required(login_url='/')
def manage_company(request):
    context = {
        'company': getCompany(),
        'dec_form': DecForm(),
        'company_image_form': CompanyImageForm(instance=getCompany()),
        'menus': set_menus('manage_company')
    }

    if request.method == 'GET':
        return render(request, 'app_manage/company.html', context=context)
    elif request.method == 'POST':  # 因为前端是用form表单，form表单只能用post和get，所以就用post替代put来修改数据好了
        # put_data = json.loads(list(request.POST.keys())[0])   # 用表单提交的数据直接就是字典形式，不需要转换
        put_data = request.POST
        print('接收到post修改的公司信息：', put_data)

        # 先更新两张图片的数据
        company_image_form = CompanyImageForm(request.POST, request.FILES, instance=context['company'])
        if company_image_form.is_valid():
            company_image_form.save()

        # 后更新其余数据
        name_list = ['name', 'slogan', 'email', 'telephone', 'phone', 'dec']
        modifily_data(name_list, put_data, Company, context['company'].id)

        return HttpResponseRedirect('/manage')
    else:
        print('???not get and not post? what are you doing?')
        return HttpResponseRedirect('/')


@login_required(login_url='/')
def manage_abstract_text(request):
    context = {
        'menus': set_menus('manage_abstract_text'),
        'abstract_texts': AbstractText.objects.all()
    }

    if request.method == 'GET':
        return render(request, 'app_manage/abstract_text.html', context=context)
    elif request.method == 'POST':
        try:
            print('接收到post新增摘要数据：', request.POST)
            AbstractText.objects.create(**json.loads(list(request.POST.keys())[0]))

            return JsonResponse({'message': None})
        except Exception:
            return JsonResponse({'message': '添加数据失败！请重试'})
    elif request.method == 'PUT':
        try:
            name_list = ['title', 'title2', 'content']
            put_data = json.loads(list(QueryDict(request.body).keys())[0])
            print('接收到put修改摘要数据：', put_data)

            modifily_data(name_list, put_data, AbstractText, put_data['id'])

            return JsonResponse({'message': None})
        except Exception:
            return JsonResponse({'message': '修改数据失败！请重试'})
    elif request.method == 'DELETE':
        try:
            delete_data = json.loads(list(QueryDict(request.body).keys())[0])
            print('将删除的摘要数据的id为：', delete_data)
            AbstractText.objects.filter(id=delete_data['id']).delete()
            return JsonResponse({'message': None})
        except Exception:
            return JsonResponse({'message': '删除数据失败！请重试'})
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
def manage_category(request):
    context = {
        'menus': set_menus('manage_category'),
        'menu1s': getMenu1s(),
        'module1': Module.objects.filter(name='首页模块一'),
        'module2': Module.objects.filter(name='首页模块二'),
    }

    if request.method == 'GET':
        return render(request, 'app_manage/category.html', context=context)
    elif request.method == 'POST':  # 前端传入的新增数据是列表
        post_datas = json.loads(list(request.POST.keys())[0])
        print('接收到post新增的分类数据：', post_datas, type(post_datas))

        for post_data in post_datas:
            Category.objects.create(**post_data)

        return JsonResponse({'message': None})
    elif request.method == 'PUT':
        put_datas = json.loads(list(QueryDict(request.body).keys())[0])
        print('接收到put修改的分类数据：', put_datas, type(put_datas))

        name_list = ['name', 'parent_id']
        for put_data in put_datas:
            modifily_data(name_list, put_data, Category, put_data['id'])

        return JsonResponse({'message': None})
    elif request.method == 'DELETE':
        try:
            delete_data = json.loads(list(QueryDict(request.body).keys())[0])
            print('将删除的菜单分类数据的id为：', delete_data)
            Category.objects.filter(id=delete_data['id']).delete()
            return JsonResponse({'message': None})
        except Exception:
            return JsonResponse({'message': '删除数据失败！请重试'})
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
        'carousels': Carousel.objects.all().order_by('number')
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
def manage_carousel(request):
    if request.method == 'POST':  # 前端传入的新增数据是要设为轮播图的文章id
        put_data = json.loads(list(request.POST.keys())[0])
        print('接收到post新增的轮播图文章id：', put_data, type(put_data))

        article = Article.objects.get(id=put_data['article_id'])
        carousels = Carousel.objects.filter(article=article)
        if not carousels:
            number = len(Carousel.objects.all()) + 1
            Carousel.objects.create(img=article.cover_img, title=article.title, article=article, number=number)

        return JsonResponse({'message': None})
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
    all_menus = Category.objects.all()
    menu12s = []
    for menu in all_menus:
        if not menu.has_children():
            menu12s.append(menu)
    return menu12s


@login_required(login_url='/')
def write_article(request):     # 新建文章
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
def manage_article(request, id):    # 修改文章
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
        return HttpResponseRedirect('/manage/manage_article/'+id)
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

    context['articles'] = Article.objects.filter(category_id=id).order_by('modified_time')

    return render(request, 'app_manage/articles.html', context=context)


def set_module(name, category_id):
    module = Module.objects.filter(name=name)
    print(category_id)
    if category_id == '----空----':
        print('删除')
        module.delete()
    else:
        if module:
            module = module[0]
            module.category_id = category_id
            module.save()
        else:
            Module.objects.create(name=name, category_id=category_id)


@login_required(login_url='/')
def set_module1(request):
    if request.method == 'POST':  # 前端是form表单提交
        post_data = request.POST
        print('接收到post的设置模块1数据：', post_data)

        name = '首页模块一'
        set_module(name, post_data['category_id'])

        return HttpResponseRedirect('/manage/manage_category')


@login_required(login_url='/')
def set_module2(request):
    if request.method == 'POST':  # 前端是form表单提交
        post_data = request.POST
        print('接收到post的设置模块2数据：', post_data)

        name = '首页模块二'
        set_module(name, post_data['category_id'])

        return HttpResponseRedirect('/manage/manage_category')



class LoginView(View):
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
