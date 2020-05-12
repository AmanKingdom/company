from django.forms import Form, fields, forms, ModelForm
from DjangoUeditor.forms import UEditorField

from app1.models import Company, Wechat, Article, Carousel


class LoginForm(Form):
    username = fields.CharField()
    password = fields.CharField()


class ContentForm(forms.Form):
    content = UEditorField("", height=500, width=830, toolbars='besttome')


class CompanyImageForm(ModelForm):
    class Meta:
        model = Company
        labels = {
            'logo': '',
        }
        fields = ['logo', ]


class CarouselImageForm(ModelForm):
    class Meta:
        model = Carousel
        labels = {
            'img': '',
        }
        fields = ['img', ]


class WechatImageForm(ModelForm):
    class Meta:
        model = Wechat
        labels = {
            'qrcode': '',
            'logo': ''
        }
        fields = ['qrcode', 'logo']


class ArticleImageForm(ModelForm):
    class Meta:
        model = Article
        labels = {
            'cover_img': '',
        }
        fields = ['cover_img', ]
