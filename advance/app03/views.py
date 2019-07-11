from django.shortcuts import render,redirect,HttpResponse
from functools import wraps
from django import views
# Create your views here.
# Django提供的工具，把函数装饰器转变成方法装饰器
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt
#csrf_exempt，取消当前函数防跨站请求伪造功能，即便settings中设置了全局中间件。
def login(request):
    print(request.get_full_path())  # 获取当前请求的路径和参数
    print(request.path_info)  # 取当前请求的路径
    print("-" * 120)
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        next = request.GET.get("next")
        print(username,password)
        if username =='xiaoqian' and password == '123':

            if next:
                rep = redirect(next)
            else:
                rep = redirect('/display/')
            request.session['is_login'] = '1'
            request.session['user'] = username
            request.session.set_expiry(7)
            return rep
    return render(request,'login1.html')


def check_login(func):
    wraps(func)  # 装饰器修复技术
    def inner(request,*args,**kwargs):
        ret = request.session.get("is_login")
        if ret =='1':
            return func(request,*args,**kwargs)
        else:
            #拼接登录成功后需要转到的url字符串
            next_url=request.path_info
            return redirect('/login/?next={}'.format(next_url))

    return inner

#display = check_login(display)
@check_login
def display(request):
    return render(request,'display.html')


def logout(request):
    request.session.flush()
    return redirect('/login/')


# @method_decorator(check_login, name="get")
class UserInfo(views.View):
   #在CBV中使用装饰器
    @method_decorator(check_login)
    def get(self, request):
        return render(request, "userinfo.html")