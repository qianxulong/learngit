from django.shortcuts import render,redirect,HttpResponse
from app01 import models

# Create your views here.
def page(request):
    page_num = request.GET.get("page")
    count = models.Book.objects.all().count()
    from footprint.mypage import Page
    page_obj = Page(page_num,count,'/page/')
    page_html = page_obj.page_html()
    #在queryset情况下才能切片
    books = models.Book.objects.all()[page_obj.start:page_obj.end]
    return render(request,'book.html',{'books':books,'page_html':page_html})

def login(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        print(username,password)
        if username =='xiaoqian' and password == '123':
          rep = redirect('/book/')
          rep.set_signed_cookie(key='login',value='123',salt='denglu')
          return rep
    return render(request,'login1.html')


def display(request):
    ret = request.get_signed_cookie(key='login',default='0',salt = 'denglu')
    if ret =='123':
        return render(request,'display.html')
    else:
        return redirect('/log/')


def index(request):
    if request.method =="POST":
        i1 = request.POST .get("i1")
        i2 = request.POST.get("i2")
        ret = int(i1)+int(i2)
        return HttpResponse(ret)
    return render(request,'index.html')

def check1(request):
    if request.method =="POST":
        name = request.POST.get("name")
        a = models.Author.objects.all().values_list("name")
        name_list = []
        for i in a:
            name_list.append(i[0])
        print(name_list)
        if name in name_list:
            msg = '您的用户名已被占用'
            print(msg)
        else:
            msg =""
        return HttpResponse(msg)

def check2(request):
    if request.method=="POST":
        p1 =request.POST.get("p1")
        i4 =request.POST.get("i4")
        print(p1,i4)
        arg ={}
        if i4:
            if p1:
                arg['msg']= '请再次确认用户名'
                arg['status']=1
                print(arg)
            else:
                models.Author.objects.create(name=i4)
                arg['msg']= '注册成功'
                arg['status'] = 2
                print(arg)
        else:
            arg['msg'] ='请先输入用户名'
            arg['status'] = 0
            print(arg)
        import json
        msg =json.dumps(arg)
        return HttpResponse(msg)

from django import forms
from django.forms import widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
class RegForm(forms.Form):
    name = forms.CharField(
        # 校验规则相关
        max_length=16,
        label="用户名",
        error_messages={
            "required": "该字段不能为空",
        },
        # widget控制的是生成html代码相关的
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    pwd = forms.CharField(
        label="密码",
        min_length=6,
        max_length=10,
        widget=widgets.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        error_messages={
            "min_length": "密码不能少于6位！",
            "max_length": "密码最长10位！",
            "required": "该字段不能为空",
        }
    )
    re_pwd = forms.CharField(
        label="确认密码",
        min_length=6,
        max_length=10,
        widget=widgets.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        error_messages={
            "min_length": "密码不能少于6位！",
            "max_length": "密码最长10位！",
            "required": "该字段不能为空",
        }
    )
    email = forms.EmailField(
        label='邮箱',
        error_messages={
            "required":"该字段不能为空",
            "invalid":'格式有误'
        },
        widget=widgets.EmailInput(attrs={"class":"form-control"})

    )
    mobile = forms.CharField(
        label="手机号",
        #RegexValidator验证器
        validators=[RegexValidator(r'^[0-9]+$','手机号必须全是数字'),
                    RegexValidator(r'^[1][^0-2][0-9]{9}','手机号格式有误')],
        widget = widgets.TextInput(attrs={"class":"form-control"}),
        error_messages = {"required": "该字段不能为空"}
    )
    # 还可以在Form类中定义钩子函数，来实现自定义的验证功能。

    #定义局部钩子
    def clean_name(self):
        value = self.cleaned_data.get("name")
        if "高高" in value:
            raise ValidationError("你为什么要输这个")
        else:
            return value

    # 定义全局的钩子，用来校验密码和确认密码字段是否相同
    def clean(self):
        pwd =self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")
        if pwd ==re_pwd:
            return self.cleaned_data
        else:
            self.add_error('re_pwd','两次密码输入不一致')

            raise ValidationError("两次密码输入不一致")


    city = forms.ChoiceField(
            choices=models.City.objects.all().values_list("id", "name"),
            label="城市",
            initial=1,
            widget=forms.widgets.Select
        )
    #需要注意choices的选项可以配置从数据库中获取，但是由于是静态字段
    #获取的值无法实时更新，需要重写构造方法从而实现choice实时更新。

    # 重写父类的init方法

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["city"].choices = models.City.objects.all().values_list("id", "name")


def reg2(request):
    form_obj = RegForm()

    if request.method == "POST":
        form_obj = RegForm(request.POST)

        # 让form帮我们做校验
        if form_obj.is_valid():
            # 校验通过
            # 把数据存到数据库
            # 所有经过校验的数据都保存在 form_obj.cleaned_data
            print(form_obj.cleaned_data)
            del form_obj.cleaned_data["re_pwd"]
            models.UserInfo.objects.create(**form_obj.cleaned_data)
            return HttpResponse("注册成功！")
        print(form_obj.cleaned_data)
    return render(request, "reg2.html", {"form_obj": form_obj})


# # 自定义验证规则
# def mobile_validate(value):
#     mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
#     if not mobile_re.match(value):
#         raise ValidationError('手机号码格式错误')
#
#
# class PublishForm(Form):
#     title = fields.CharField(max_length=20,
#                              min_length=5,
#                              error_messages={'required': '标题不能为空',
#                                              'min_length': '标题最少为5个字符',
#                                              'max_length': '标题最多为20个字符'},
#                              widget=widgets.TextInput(attrs={'class': "form-control",
#                                                              'placeholder': '标题5-20个字符'}))
#
#     # 使用自定义验证规则
#     phone = fields.CharField(validators=[mobile_validate, ],
#                              error_messages={'required': '手机不能为空'},
#                              widget=widgets.TextInput(attrs={'class': "form-control",
#                                                              'placeholder': u'手机号码'}))
#
#     email = fields.EmailField(required=False,
#                               error_messages={'required': u'邮箱不能为空', 'invalid': u'邮箱格式错误'},
#                               widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': u'邮箱'}))


# 批量添加样式
# class LoginForm(forms.Form):
#     username = forms.CharField(
#         min_length=8,
#         label="用户名",
#         initial="张三",
#         error_messages={
#             "required": "不能为空",
#             "invalid": "格式错误",
#             "min_length": "用户名最短8位"
#         }
#     ...
#
#     def __init__(self, *args, **kwargs):
#         super(LoginForm, self).__init__(*args, **kwargs)
#         for field in iter(self.fields):
#             self.fields[field].widget.attrs.update({
#                 'class': 'form-control'
#             })

