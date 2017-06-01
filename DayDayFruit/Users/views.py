#coding:utf-8

from django.shortcuts import render, redirect
from models import *
from django.http import JsonResponse



def index(request):
    return render(request, 'Users/index.html')


def login(request):
    context = {'uname_err_code':0, 'pwd_err_code':0}
    return render(request, 'Users/login.html', context)

def login_handle(request):
    from hashlib import sha1
    flage = True
    context = {}

    if request.method == 'POST':
        dict = request.POST
        user_name = dict.get('username','')
        pwd = dict.get('pwd')
        # 加密
        sha1 = sha1()
        sha1.update(pwd)
        pwd = sha1.hexdigest()

        # 检查用户名输入是否正确
        uname_err_code = check_user_for_login(user_name)
        if uname_err_code > 0:
            flage = False
            context['uname_err_code'] = uname_err_code
            context['uname'] = user_name
        else:
            context['uname_err_code'] = 0  # 正确返回0

        # 检查密码是否正确
        if user_name:
            if uname_err_code == 0:
                user = Users.objects.filter(uname=user_name)
                pword = user[0].pword
                if pword != pwd:
                    flage = False
                    context['pwd_err_code'] = 1
                else:
                    context['pwd_err_code'] = 0
            else:
                context['uname_err_code'] = 3
                context['pwd_err_code'] = 0
        else:
            context['uname_err_code'] = 1
            context['pwd_err_code'] = 0

        # 如果登陆成功跳转到首页，　否则返回错误信息
        if flage:
            return redirect('/')
        else:
            return render(request, 'Users/login.html', context)



# 渲染register页面
def register(request):
    context = {'uname_err_code':0, 'pwd_err_code':0}
    return render(request, 'Users/register.html', context)

# 检查用户是否存在，存在返回大于０
def user_exit(request):
    user_name = request.GET.get('user_name')
    count = Users.objects.filter(uname=user_name).count()
    return JsonResponse({'count':count})

# 用户注册
def register_handle(request):
    from hashlib import sha1
    flage = True
    context = {}

    if request.method == 'POST':
        # 获取输入的内容
        dict = request.POST
        user_name = dict.get('user_name')
        pwd = dict.get('pwd')
        cpwd = dict.get('cpwd')
        email = dict.get('email')

        # 检查用户名输入是否正确
        uname_err_code = check_user_name(user_name)
        if uname_err_code > 0:
            flage = False
            context['uname_err_code'] = uname_err_code
        else:
            context['uname_err_code'] = 0  # 正确返回0

        # 检查密码是否正确
        if pwd != cpwd:
            flage = False
            context['pwd_err_code'] = 1  # 错误返回１
        else:
            context['pwd_err_code'] = 0  # 正确返回0
        
        # 如果用户名和密码都正确，则提交到数据库
        if flage:
            user = Users()
            user.uname = user_name
            # 加密
            sha1 = sha1()
            sha1.update(pwd)
            pwd = sha1.hexdigest()

            user.pword = pwd
            user.email = email
            user.save()
            return redirect('/user/login/')
        else:
            # 否则将错误信息返回给前台页面
            return render(request, 'Users/register.html', context)


# 后台检查用户名是否正确
def check_user_name(user_name):
    if user_name == "":
        # "用户名不能为空！"
        return 1
    elif len(user_name) < 5 or len(user_name) > 20:
        # "用户名长度必须大于5且小于20！"
        return 2

    count = Users.objects.filter(uname=user_name).count()
    if count >= 1:
        # "用户名已经存在,请重新输入！"
        return 3
    else:
        return 0

def check_user_for_login(user_name):
    if user_name == "":
        # "用户名不能为空！"
        return 1
    elif len(user_name) < 5 or len(user_name) > 20:
        # "用户名长度必须大于5且小于20！"
        return 2

    count = Users.objects.filter(uname=user_name).count()
    if count == 0:
        return 3   # 用户不存在
    else:
        return 0
