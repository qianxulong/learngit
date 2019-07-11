from django.shortcuts import render,redirect,HttpResponse
from app01 import models

# Create your views here.
def login(request):
    ret = ''
    if request.method =='POST':
        name = request.POST.get('username')
        password = request.POST.get('pwd')
        if name == 'qian'and password == '123456':
            return redirect('/transfer/')
        else:
            ret = '请重新输入用户名或密码'
            return render(request,'login.html',{'alert':ret})
    return render(request,'login.html')

def transfer(request):
    if request.method == 'POST':
        Out = request.POST.get('from')
        In = request.POST.get('to')
        money =request.POST.get('money')
        return HttpResponse('{}成功转给{}{}'.format(Out,In,money))
    return render(request,'transfer.html')


def page(request):
    book_num = models.Book.objects.all().count()
    max_per_book = 10
    page_total,m =divmod(book_num,max_per_book)
    if m:
        page_total += 1
    page_num = request.GET.get("id")
    try:
        page_num = int(page_num)
        if page_num> page_total:
            page_num = page_total
        if page_num <=0:
            page_num=1
    except Exception as e:
        page_num = 1

    max_page = 11
    if page_total <max_page:
        max_page =page_total

    page_middle = max_page//2
    page_start = page_num - page_middle
    page_end = page_num + page_middle
    if page_start < 1:
        page_start = 1
        page_end  =page_start + max_page-1
    if page_end > page_total:
        page_end =page_total
        page_start  =page_end - max_page+1
    html_str_list =[]
    html_str_list.append('<li><a href="/book/?id=1">首页</a></li>')
    if page_num <= 1:
        html_str_list.append('<li class="disabled"><a href="#">上一页</a></li>')
    else:
        html_str_list.append('<li><a href="/book/?id={}">上一页</a></li>'.format(page_num-1))
    for i in range(page_start,page_end+1):
        if i ==page_num:
            tmp = '<li class="active"><a href="/book/?id={0}">{0}</a></li>'.format(i)
        else:
            tmp = '<li><a href="/book/?id={0}">{0}</a></li>'.format(i)

        html_str_list.append(tmp)
    if page_num>= page_total:
        html_str_list.append('<li class="disabled"><a href="/book/?id={}">下一页</a></li>'.format(page_num+1))
    else:
        html_str_list.append('<li ><a href="/book/?id={}">下一页</a></li>'.format(page_num - 1))
    html_str_list.append('<li ><a href="/book/?id={}">尾页</a></li>'.format(page_total))

    page_html = "".join(html_str_list)
    print(page_html)

    book_start = (page_num-1)*10
    book_end = page_num*10
    books = models.Book.objects.all()[book_start:book_end]
    return render(request,'book.html',{'books':books,'page_html':page_html})