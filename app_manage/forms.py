from django.forms import Form, fields, forms, ModelForm
from DjangoUeditor.forms import UEditorField

from app1.models import Company, Wechat, Article


class LoginForm(Form):
    username = fields.CharField()
    password = fields.CharField()


class DecForm(forms.Form):
    dec = UEditorField("", initial="", height=200, toolbars="besttome")


class ContentForm(forms.Form):
    content = UEditorField("", height=500, width=830, toolbars='besttome')


class CompanyImageForm(ModelForm):
    class Meta:
        model = Company
        labels = {
            'logo': '',
            'big_img': ''
        }
        fields = ['logo', 'big_img']


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
