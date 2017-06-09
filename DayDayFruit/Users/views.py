# coding:utf-8

from django.shortcuts import render, redirect
from models import *
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from . import user_decorator
from df_order.models import *


def index(request):
    return redirect('/goods/index/')


def login(request):
    context = {'uname_err_code': 0, 'pwd_err_code': 0}
    return render(request, 'Users/login.html', context)


# 注销用户
def logout(request):
    request.session.flush()
    return redirect('/user/login/')


def login_handle(request):
    from hashlib import sha1
    flage = True
    context = {}
    user = None

    if request.method == 'POST':
        dict = request.POST
        user_name = dict.get('username', '')
        pwd = dict.get('pwd')
        # 加密
        sha1 = sha1()
        sha1.update(pwd)
        pwd = sha1.hexdigest()
        rember_me = dict.get('rember_me', 0)

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
            url = request.COOKIES.get('url', '/user/')
            red = HttpResponseRedirect(url)
            # 成功后删除转向地址，防止以后直接登录造成的转向
            red.set_cookie('url', '', max_age=-1)

            if rember_me:
                red.set_cookie('uname', user_name)
            else:
                red.set_cookie('uname', '', max_age=-1)

            request.session['user_id'] = user[0].id
            request.session['user_name'] = user_name
            return red
            # return redirect('/user/')
        else:
            return render(request, 'Users/login.html', context)


# 渲染register页面
def register(request):
    context = {'uname_err_code': 0, 'pwd_err_code': 0}
    return render(request, 'Users/register.html', context)


# 检查用户是否存在，存在返回大于０
def user_exit(request):
    user_name = request.GET.get('user_name')
    count = Users.objects.filter(uname=user_name).count()
    return JsonResponse({'count': count})


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
        return 3  # 用户不存在
    else:
        return 0


@user_decorator.login
def user_center_info(request):
    uname = ''
    phone = ''
    address = ''

    uid = request.session.get('user_id', 0)
    if uid:
        user = Users.objects.filter(id=uid)
        if user.count:
            uname = user[0].uname
            phone = user[0].phone
            address = user[0].address

        goods = VisitInfo.objects.filter(vusers_id=uid).order_by('-vclick')
        if goods.count <= 5:
            goods_list = goods
        else:
            goods_list = goods[0:5]
    context = {'uname': uname, 'phone': phone, 'address': address, 'page_num': 1, 'goods_list': goods_list,
               'title': '用户中心'}
    return render(request, 'Users/user_center_info.html', context)


@user_decorator.login
def user_center_site(request):
    contact = ''
    phone = ''
    address = ''
    postcode = ''

    uid = request.session.get('user_id', 0)
    if uid:
        user = Users.objects.filter(id=uid)
        if user.count:
            phone = user[0].phone
            address = user[0].address
            contact = user[0].contact
            postcode = user[0].postcode
    context = {'contact': contact, 'phone': phone, 'address': address, 'postcode': postcode, 'page_num': 1,
               'title': '用户中心'}
    return render(request, 'Users/user_center_site.html', context)


@user_decorator.login
def user_center_site_handle(request):
    uid = request.session.get('user_id', 0)
    contact = ''
    phone = ''
    address = ''
    postcode = ''

    if request.method == 'POST':
        contact = request.POST.get('contact', '')
        address = request.POST.get('address', '')
        postcode = request.POST.get('postcode', '')
        phone = request.POST.get('phone', '')

        if uid:
            user = Users.objects.get(id=uid)
            user.contact = contact
            user.address = address
            user.postcode = postcode
            user.phone = phone
            user.save()

    context = {'contact': contact, 'phone': phone, 'address': address, 'postcode': postcode, 'page_num': 1}
    return render(request, 'Users/user_center_site.html', context)

@user_decorator.login
def user_center_order(request):
    user_id = request.session.get('user_id')
    orders = OrderInfo.objects.filter(user_id=user_id)

    context = {'title': '用户中心', 'page_num': 1, 'orders': orders}
    return render(request, 'Users/user_center_order.html', context)