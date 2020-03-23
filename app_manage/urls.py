from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import manage_company, LoginView, logout_view, manage_abstract_text, manage_wechat, manage_category, \
    manage_articles, manage_article, write_article, select_category, manage_carousel, set_module1, set_module2

urlpatterns = [
    path('', manage_company, name='manage_company'),    # 本项目的/manage首页就为公司信息管理
    path('manage_abstract_text/', manage_abstract_text, name='manage_abstract_text'),
    path('manage_wechat/', manage_wechat, name='manage_wechat'),
    path('manage_category/', manage_category, name='manage_category'),
    path('manage_articles/', manage_articles, name='manage_articles'),
    path('manage_carousel/', manage_carousel, name='manage_carousel'),
    path('write_article/', write_article, name='write_article'),
    path('manage_article/<id>/', manage_article, name='manage_article'),
    path('select_category/<id>/', select_category, name='select_category'),
    path('set_module1', set_module1, name='set_module1'),
    path('set_module2', set_module2, name='set_module2'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)