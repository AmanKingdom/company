from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import manage_company, LoginView, logout_view, manage_wechat, init_menu,\
    manage_articles, manage_article, write_article, select_category, manage_carousel

urlpatterns = [
    path('init_menu/', init_menu, name='init_menu'),
    path('', manage_company, name='manage_company'),    # 本项目的/manage首页就为公司信息管理
    path('manage_wechat/', manage_wechat, name='manage_wechat'),
    path('manage_articles/', manage_articles, name='manage_articles'),
    path('manage_carousel/', manage_carousel, name='manage_carousel'),
    path('write_article/', write_article, name='write_article'),
    path('manage_article/<id>/', manage_article, name='manage_article'),
    path('select_category/<id>/', select_category, name='select_category'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)